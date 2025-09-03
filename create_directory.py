from pathlib import Path
import gdsfactory as gf
import json

def create_wafer_dir(gds: gf.Component, dir_name: str, design_json: str) -> None:
    
    # Specify the nested directory structure
    main_dir_path = Path("I:\\SergeR_Group\\Notes\\Fabrication\\" + dir_name)

    # Create nested directories
    main_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{main_dir_path}' created successfully.")

    design_dir_path = main_dir_path.joinpath("Design")
    design_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Nested directories '{design_dir_path}' created successfully.")

    gds.write_gds(design_dir_path.joinpath("testing.gds"), with_metadata=False)

    with design_dir_path.joinpath("data.json").open("w", encoding ="utf-8") as f:
        f.write(design_json)

def create_design_json(wafer_name: str,
                       wafer_material: str,
                       wafer_size: float,
                       wafer_thickness: str,
                       recipe: str,
                       sample_names: list,
                       sample_dimension: str,
                       sample_center: str,
                       sample_jopherson_junctions: list,
                       test_junctions: dict
                       ) -> str:
        # Json to have:
        # wafer name
        # material 
        # size
        # thickness
        # recipe
        # sample names 
        # sample Dimension
        # sample center
        #   jj_N style
        #   jj_N width
        #   jj_N gap
        # test junctions:
        #   type:
        #       DOLAN
        #       DOLATHAN
        #       MANHANTAN
        #    BRIDGE START GAP
        #    BRIDGE END GAP
        #    FINGER WIDTH
    rtn: dict = {}
    rtn['wafer name'] = wafer_name
    rtn['material'] = wafer_material
    rtn['size'] = wafer_size
    rtn['thickness'] = wafer_thickness
    rtn['recipe'] = recipe
    rtn['sample names'] = sample_names
    rtn['sample dimension'] = sample_dimension
    rtn['sample center'] = sample_center
    rtn['sample jopherson junctions'] = sample_jopherson_junctions
    rtn['test junctions'] = test_junctions

    return json.dumps(rtn)