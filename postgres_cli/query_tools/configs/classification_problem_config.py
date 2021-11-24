base_config = {
    "detection_problem": False,
    "classification_problem": True,
    "barkbeetle_problem": False,
    "make_label_mappings": {
        "label_path": "TODO Path to the primary lables, that will be used to determin the classes"
    },
    "Albunet": {
        "resnet_size": 18,
        "pretrained": True, 
    },
    "adam": {"lr": 0.001},
    "make_loader": {"batch_size": 12},
    "do_training": {"epochs": 1500}, 
    "make_dataset_max_size": 8,
}


