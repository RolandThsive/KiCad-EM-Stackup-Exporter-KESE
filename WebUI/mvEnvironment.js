/* mvEnvironment.js - <model-viewer>'s default lighting, taken out of model-viewer 4.4.0 so a plain three.js
   viewer draws a GLB exactly as <model-viewer> does with no environment-image set.
   From @google/model-viewer lib/three-components/TextureUtils.js (GenerateEnvironmentMap, blurCubemap,
   halfblur, getBlurShader) and Renderer.js (tone mapping and exposure).
   Copyright 2021 Google LLC, Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0). */
import { BackSide, BoxGeometry, CubeCamera, HalfFloatType, LinearSRGBColorSpace, Mesh, NoBlending, NoToneMapping,
  NeutralToneMapping, RGBAFormat, Scene, ShaderMaterial, Vector3, WebGLCubeRenderTarget } from 'three';
import EnvironmentScene from './NeutralEnvironment.js';

const GENERATED_SIGMA = 0.04;
const MAX_SAMPLES = 20;
const COMMERCE_EXPOSURE = 1.3;   // Renderer.js: the exposure model-viewer uses with its own neutral studio

class EnvBuilder {
  constructor(threeRenderer) { this.threeRenderer = threeRenderer; }
    blurCubemap(cubeTarget, sigma) {
        if (this.blurMaterial == null) {
            this.blurMaterial = this.getBlurShader(MAX_SAMPLES);
            const box = new BoxGeometry();
            const blurMesh = new Mesh(box, this.blurMaterial);
            this.blurScene = new Scene();
            this.blurScene.add(blurMesh);
        }
        const tempTarget = cubeTarget.clone();
        this.halfblur(cubeTarget, tempTarget, sigma, 'latitudinal');
        this.halfblur(tempTarget, cubeTarget, sigma, 'longitudinal');
        // Disposing this target after we're done with it somehow corrupts Safari's
        // whole graphics driver. It's random, but occurs more frequently on
        // lower-powered GPUs (macbooks with intel graphics, older iPhones). It goes
        // beyond just messing up the PMREM, as it also occasionally causes
        // visible corruption on the canvas and even on the rest of the page.
        /** tempTarget.dispose(); */
    }
    halfblur(targetIn, targetOut, sigmaRadians, direction) {
        // Number of standard deviations at which to cut off the discrete
        // approximation.
        const STANDARD_DEVIATIONS = 3;
        const pixels = targetIn.width;
        const radiansPerPixel = isFinite(sigmaRadians) ?
            Math.PI / (2 * pixels) :
            2 * Math.PI / (2 * MAX_SAMPLES - 1);
        const sigmaPixels = sigmaRadians / radiansPerPixel;
        const samples = isFinite(sigmaRadians) ?
            1 + Math.floor(STANDARD_DEVIATIONS * sigmaPixels) :
            MAX_SAMPLES;
        if (samples > MAX_SAMPLES) {
            console.warn(`sigmaRadians, ${sigmaRadians}, is too large and will clip, as it requested ${samples} samples when the maximum is set to ${MAX_SAMPLES}`);
        }
        const weights = [];
        let sum = 0;
        for (let i = 0; i < MAX_SAMPLES; ++i) {
            const x = i / sigmaPixels;
            const weight = Math.exp(-x * x / 2);
            weights.push(weight);
            if (i == 0) {
                sum += weight;
            }
            else if (i < samples) {
                sum += 2 * weight;
            }
        }
        for (let i = 0; i < weights.length; i++) {
            weights[i] = weights[i] / sum;
        }
        const blurUniforms = this.blurMaterial.uniforms;
        blurUniforms['envMap'].value = targetIn.texture;
        blurUniforms['samples'].value = samples;
        blurUniforms['weights'].value = weights;
        blurUniforms['latitudinal'].value = direction === 'latitudinal';
        blurUniforms['dTheta'].value = radiansPerPixel;
        const cubeCamera = new CubeCamera(0.1, 100, targetOut);
        cubeCamera.update(this.threeRenderer, this.blurScene);
    }
    getBlurShader(maxSamples) {
        const weights = new Float32Array(maxSamples);
        const poleAxis = new Vector3(0, 1, 0);
        const shaderMaterial = new ShaderMaterial({
            name: 'SphericalGaussianBlur',
            defines: { 'n': maxSamples },
            uniforms: {
                'envMap': { value: null },
                'samples': { value: 1 },
                'weights': { value: weights },
                'latitudinal': { value: false },
                'dTheta': { value: 0 },
                'poleAxis': { value: poleAxis }
            },
            vertexShader: /* glsl */ `
      
      varying vec3 vOutputDirection;
  
      void main() {
  
        vOutputDirection = vec3( position );
        gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
  
      }
    `,
            fragmentShader: /* glsl */ `
        varying vec3 vOutputDirection;
  
        uniform samplerCube envMap;
        uniform int samples;
        uniform float weights[ n ];
        uniform bool latitudinal;
        uniform float dTheta;
        uniform vec3 poleAxis;
  
        vec3 getSample( float theta, vec3 axis ) {
  
          float cosTheta = cos( theta );
          // Rodrigues' axis-angle rotation
          vec3 sampleDirection = vOutputDirection * cosTheta
            + cross( axis, vOutputDirection ) * sin( theta )
            + axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );
  
          return vec3( textureCube( envMap, sampleDirection ) );
  
        }
  
        void main() {
  
          vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );
  
          if ( all( equal( axis, vec3( 0.0 ) ) ) ) {
  
            axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );
  
          }
  
          axis = normalize( axis );
  
          gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
          gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );
  
          for ( int i = 1; i < n; i++ ) {
  
            if ( i >= samples ) {
  
              break;
  
            }
  
            float theta = dTheta * float( i );
            gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
            gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );
  
          }
        }
      `,
            blending: NoBlending,
            depthTest: false,
            depthWrite: false,
            side: BackSide
        });
        return shaderMaterial;
    }
}

/** Sets renderer and scene up as <model-viewer> does by default. */
export function useModelViewerLook(renderer, scene) {
  renderer.toneMapping = NeutralToneMapping;
  renderer.toneMappingExposure = COMMERCE_EXPOSURE;
  const cubeTarget = new WebGLCubeRenderTarget(256, { generateMipmaps: false, type: HalfFloatType, format: RGBAFormat,
    colorSpace: LinearSRGBColorSpace, depthBuffer: true });
  const cubeCamera = new CubeCamera(0.1, 100, cubeTarget);
  const outputColorSpace = renderer.outputColorSpace;
  renderer.toneMapping = NoToneMapping;
  renderer.outputColorSpace = LinearSRGBColorSpace;
  cubeCamera.update(renderer, new EnvironmentScene('neutral'));
  new EnvBuilder(renderer).blurCubemap(cubeTarget, GENERATED_SIGMA);
  renderer.toneMapping = NeutralToneMapping;
  renderer.outputColorSpace = outputColorSpace;
  scene.environment = cubeTarget.texture;
}
