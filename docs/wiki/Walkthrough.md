# 19. Walkthrough

What each solver does with a KESE export, how to install it, and every step from the board file to L, R and M.

## 19.1 Elmer FEM

[Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md), on the [`Elmer_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Elmer_Integration) branch:

- [What Elmer Is Used For Here](Elmer-FEM-Walkthrough.md#1911-what-elmer-is-used-for-here)
- [How It Fits Together](Elmer-FEM-Walkthrough.md#1912-how-it-fits-together)
- [Where The Code Is](Elmer-FEM-Walkthrough.md#1914-where-the-code-is)
- [Linux (Ubuntu 24.04)](Elmer-FEM-Walkthrough.md#1915-linux-ubuntu-2404)
- [Windows](Elmer-FEM-Walkthrough.md#1916-windows)
- [What The Test Machines Had](Elmer-FEM-Walkthrough.md#1917-what-the-test-machines-had)
- [Export The Board With KESE](Elmer-FEM-Walkthrough.md#1918-export-the-board-with-kese)
- [Section The Parts Into Slabs](Elmer-FEM-Walkthrough.md#1919-section-the-parts-into-slabs)
- [Triangulate The Footprint](Elmer-FEM-Walkthrough.md#19110-triangulate-the-footprint)
- [Stack The Wedges, Fill The Air](Elmer-FEM-Walkthrough.md#19111-stack-the-wedges-fill-the-air)
- [Open Each Coil At Its Port](Elmer-FEM-Walkthrough.md#19112-open-each-coil-at-its-port)
- [Write The Elmer Case](Elmer-FEM-Walkthrough.md#19113-write-the-elmer-case)
- [Solve And Read Back](Elmer-FEM-Walkthrough.md#19114-solve-and-read-back)
- [A Rotor Over A Stator](Elmer-FEM-Walkthrough.md#19115-a-rotor-over-a-stator)

## 19.2 PyPEEC

[PyPEEC Walkthrough](PyPEEC-Walkthrough.md), on the [`PyPEEC_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/PyPEEC_Integration) branch:

- [What PyPEEC Is Used For Here](PyPEEC-Walkthrough.md#1921-what-pypeec-is-used-for-here)
- [How It Fits Together](PyPEEC-Walkthrough.md#1922-how-it-fits-together)
- [Where The Code Is](PyPEEC-Walkthrough.md#1924-where-the-code-is)
- [Installing On Linux (Ubuntu 24.04)](PyPEEC-Walkthrough.md#1925-installing-on-linux-ubuntu-2404)
- [Installing On Windows And macOS](PyPEEC-Walkthrough.md#1926-installing-on-windows-and-macos)
- [What The Test Machine Had](PyPEEC-Walkthrough.md#1927-what-the-test-machine-had)
- [Export The Board With KESE](PyPEEC-Walkthrough.md#1928-export-the-board-with-kese)
- [Place The Parts](PyPEEC-Walkthrough.md#1929-place-the-parts)
- [Section The Parts Into Slabs](PyPEEC-Walkthrough.md#19210-section-the-parts-into-slabs)
- [Draw The Copper As Voxels](PyPEEC-Walkthrough.md#19211-draw-the-copper-as-voxels)
- [Open Each Coil At Its Port](PyPEEC-Walkthrough.md#19212-open-each-coil-at-its-port)
- [Write PyPEEC's Case](PyPEEC-Walkthrough.md#19213-write-pypeecs-case)
- [Solve And Read Back](PyPEEC-Walkthrough.md#19214-solve-and-read-back)

## 19.3 FastHenry

[FastHenry Walkthrough](FastHenry-Walkthrough.md), on the [`FastHenry_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/FastHenry_Integration) branch:

- [What FastHenry Is Used For Here](FastHenry-Walkthrough.md#1931-what-fasthenry-is-used-for-here)
- [How It Fits Together](FastHenry-Walkthrough.md#1932-how-it-fits-together)
- [Where The Code Is](FastHenry-Walkthrough.md#1934-where-the-code-is)
- [Installing On Linux (Ubuntu 24.04)](FastHenry-Walkthrough.md#1935-installing-on-linux-ubuntu-2404)
- [Installing On Windows](FastHenry-Walkthrough.md#1936-installing-on-windows)
- [What The Test Machine Had](FastHenry-Walkthrough.md#1937-what-the-test-machine-had)
- [Export The Stack-Up With KESE](FastHenry-Walkthrough.md#1938-export-the-stack-up-with-kese)
- [Read The Copper From The Board File](FastHenry-Walkthrough.md#1939-read-the-copper-from-the-board-file)
- [Build The Filament Model](FastHenry-Walkthrough.md#19310-build-the-filament-model)
- [Open Each Coil At Its Port](FastHenry-Walkthrough.md#19311-open-each-coil-at-its-port)
- [Write FastHenry's Input](FastHenry-Walkthrough.md#19312-write-fasthenrys-input)
- [Solve And Read Back](FastHenry-Walkthrough.md#19313-solve-and-read-back)
- [SIN, COS And The Angle Error](FastHenry-Walkthrough.md#19314-sin-cos-and-the-angle-error)

## 19.4 Palace

[Palace Walkthrough](Palace-Walkthrough.md), on the [`Palace_Integration`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Palace_Integration) branch:

- [What Palace Is Used For Here](Palace-Walkthrough.md#1941-what-palace-is-used-for-here)
- [How It Fits Together](Palace-Walkthrough.md#1942-how-it-fits-together)
- [Where The Code Is](Palace-Walkthrough.md#1944-where-the-code-is)
- [The Committed Build](Palace-Walkthrough.md#1945-the-committed-build)
- [Linux (Ubuntu 24.04)](Palace-Walkthrough.md#1946-linux-ubuntu-2404)
- [Building Palace From Source](Palace-Walkthrough.md#1947-building-palace-from-source)
- [Why It Is Built Without ParMETIS](Palace-Walkthrough.md#1948-why-it-is-built-without-parmetis)
- [Windows](Palace-Walkthrough.md#1949-windows)
- [What The Test Machine Had](Palace-Walkthrough.md#19410-what-the-test-machine-had)
- [Export The Board With KESE](Palace-Walkthrough.md#19411-export-the-board-with-kese)
- [Place The Parts](Palace-Walkthrough.md#19412-place-the-parts)
- [Build The 2.5D Mesh](Palace-Walkthrough.md#19413-build-the-25d-mesh)
- [Open Each Coil At Its Port](Palace-Walkthrough.md#19414-open-each-coil-at-its-port)
- [Write Palace's Input](Palace-Walkthrough.md#19415-write-palaces-input)
- [Solve And Read Back](Palace-Walkthrough.md#19416-solve-and-read-back)

| Previous | Next |
|:---|---:|
| [Feature Test Collection](Feature-Test-Collection.md) | [Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md) |
