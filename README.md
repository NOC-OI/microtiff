# microtiff
A Python module and CLI tool for converting proprietary microscopy formats to TIFF.

## Supported data types
Both supported modules and modules working with errata are listed below.

| Sensor | Status | Errata/Notes |
| --- | --- | --- |
| Imaging FlowCytobot/IFCB (.adc, .hdr, .roi) | :white_check_mark: | |
| LISST-Holo (.pgm) | :x: | Working on integration |
| LISST-Holo2 (.pgm) | :x: | Working on integration |
| FlowCam | :x: | In active development |

## Dependencies

- Pillow
- Numpy
- Holopy (for LISST-Holo/LISST-Holo2 only)

Quickly install all with the following command:
`$ pip install pillow numpy holopy`

## Acknowledgements
This library is comprised of work from various researchers.

LISST-Holo decoder based on work by [Sari Giering](https://github.com/sarigiering), [Will Major](https://github.com/obg-wrm) and [Mojtaba Masoudi](https://github.com/Mojtabamsd)
