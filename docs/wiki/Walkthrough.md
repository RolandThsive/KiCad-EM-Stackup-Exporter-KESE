# 24. Walkthrough

What each solver does with a KESE export, how to install it, and every step from the board file to L, R and M.

## 24.1 Elmer FEM

[Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md), on the [`Elmer_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Elmer_Integration) branch:

- [What Elmer Is Used For Here](Elmer-FEM-Walkthrough.md#2411-what-elmer-is-used-for-here)
- [How It Fits Together](Elmer-FEM-Walkthrough.md#2412-how-it-fits-together)
- [Where The Code Is](Elmer-FEM-Walkthrough.md#2414-where-the-code-is)
- [Linux (Ubuntu 24.04)](Elmer-FEM-Walkthrough.md#2415-linux-ubuntu-2404)
- [Windows](Elmer-FEM-Walkthrough.md#2416-windows)
- [What The Test Machines Had](Elmer-FEM-Walkthrough.md#2417-what-the-test-machines-had)
- [Export The Board With KESE](Elmer-FEM-Walkthrough.md#2418-export-the-board-with-kese)
- [Section The Parts Into Slabs](Elmer-FEM-Walkthrough.md#2419-section-the-parts-into-slabs)
- [Triangulate The Footprint](Elmer-FEM-Walkthrough.md#24110-triangulate-the-footprint)
- [Stack The Wedges, Fill The Air](Elmer-FEM-Walkthrough.md#24111-stack-the-wedges-fill-the-air)
- [Open Each Coil At Its Port](Elmer-FEM-Walkthrough.md#24112-open-each-coil-at-its-port)
- [Write The Elmer Case](Elmer-FEM-Walkthrough.md#24113-write-the-elmer-case)
- [Solve And Read Back](Elmer-FEM-Walkthrough.md#24114-solve-and-read-back)
- [A Rotor Over A Stator](Elmer-FEM-Walkthrough.md#24115-a-rotor-over-a-stator)

## 24.2 PyPEEC

[PyPEEC Walkthrough](PyPEEC-Walkthrough.md), on the [`PyPEEC_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/PyPEEC_Integration) branch:

- [What PyPEEC Is Used For Here](PyPEEC-Walkthrough.md#2421-what-pypeec-is-used-for-here)
- [How It Fits Together](PyPEEC-Walkthrough.md#2422-how-it-fits-together)
- [Where The Code Is](PyPEEC-Walkthrough.md#2424-where-the-code-is)
- [Installing On Linux (Ubuntu 24.04)](PyPEEC-Walkthrough.md#2425-installing-on-linux-ubuntu-2404)
- [Installing On Windows And macOS](PyPEEC-Walkthrough.md#2426-installing-on-windows-and-macos)
- [What The Test Machine Had](PyPEEC-Walkthrough.md#2427-what-the-test-machine-had)
- [Export The Board With KESE](PyPEEC-Walkthrough.md#2428-export-the-board-with-kese)
- [Place The Parts](PyPEEC-Walkthrough.md#2429-place-the-parts)
- [Section The Parts Into Slabs](PyPEEC-Walkthrough.md#24210-section-the-parts-into-slabs)
- [Draw The Copper As Voxels](PyPEEC-Walkthrough.md#24211-draw-the-copper-as-voxels)
- [Open Each Coil At Its Port](PyPEEC-Walkthrough.md#24212-open-each-coil-at-its-port)
- [Write PyPEEC's Case](PyPEEC-Walkthrough.md#24213-write-pypeecs-case)
- [Solve And Read Back](PyPEEC-Walkthrough.md#24214-solve-and-read-back)

## 24.3 FastHenry

[FastHenry Walkthrough](FastHenry-Walkthrough.md), on the [`FastHenry_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/FastHenry_Integration) branch:

- [What FastHenry Is Used For Here](FastHenry-Walkthrough.md#2431-what-fasthenry-is-used-for-here)
- [How It Fits Together](FastHenry-Walkthrough.md#2432-how-it-fits-together)
- [Where The Code Is](FastHenry-Walkthrough.md#2434-where-the-code-is)
- [Installing On Linux (Ubuntu 24.04)](FastHenry-Walkthrough.md#2435-installing-on-linux-ubuntu-2404)
- [Installing On Windows](FastHenry-Walkthrough.md#2436-installing-on-windows)
- [What The Test Machine Had](FastHenry-Walkthrough.md#2437-what-the-test-machine-had)
- [Export The Stack-Up With KESE](FastHenry-Walkthrough.md#2438-export-the-stack-up-with-kese)
- [Read The Copper From The Board File](FastHenry-Walkthrough.md#2439-read-the-copper-from-the-board-file)
- [Build The Filament Model](FastHenry-Walkthrough.md#24310-build-the-filament-model)
- [Open Each Coil At Its Port](FastHenry-Walkthrough.md#24311-open-each-coil-at-its-port)
- [Write FastHenry's Input](FastHenry-Walkthrough.md#24312-write-fasthenrys-input)
- [Solve And Read Back](FastHenry-Walkthrough.md#24313-solve-and-read-back)
- [SIN, COS And The Angle Error](FastHenry-Walkthrough.md#24314-sin-cos-and-the-angle-error)

## 24.4 Palace

[Palace Walkthrough](Palace-Walkthrough.md), on the [`Palace_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Palace_Integration) branch:

- [What Palace Is Used For Here](Palace-Walkthrough.md#2441-what-palace-is-used-for-here)
- [How It Fits Together](Palace-Walkthrough.md#2442-how-it-fits-together)
- [Where The Code Is](Palace-Walkthrough.md#2444-where-the-code-is)
- [The Committed Build](Palace-Walkthrough.md#2445-the-committed-build)
- [Linux (Ubuntu 24.04)](Palace-Walkthrough.md#2446-linux-ubuntu-2404)
- [Building Palace From Source](Palace-Walkthrough.md#2447-building-palace-from-source)
- [Why It Is Built Without ParMETIS](Palace-Walkthrough.md#2448-why-it-is-built-without-parmetis)
- [Windows](Palace-Walkthrough.md#2449-windows)
- [What The Test Machine Had](Palace-Walkthrough.md#24410-what-the-test-machine-had)
- [Export The Board With KESE](Palace-Walkthrough.md#24411-export-the-board-with-kese)
- [Place The Parts](Palace-Walkthrough.md#24412-place-the-parts)
- [Build The 2.5D Mesh](Palace-Walkthrough.md#24413-build-the-25d-mesh)
- [Open Each Coil At Its Port](Palace-Walkthrough.md#24414-open-each-coil-at-its-port)
- [Write Palace's Input](Palace-Walkthrough.md#24415-write-palaces-input)
- [Solve And Read Back](Palace-Walkthrough.md#24416-solve-and-read-back)

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md) |
