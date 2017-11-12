# Winnower - A Tinder AI

## Basic Workflow

1. set up "auth.json"
2. run "get_data_for_set_ranking.py"
    * Probably need about 2000 images or so
3. run "sort_images_manually.py"
    * Keep in mind: you are only liking or disliking images that are fairly unambiguous.
4. run "retrain.sh"
    * feel free to change hyper-parameters as needed
5. run "run_AI.py"
6. Profit???

## Caveats

I haven't made it sensibly deal with missing folders. I also made some changes to the Pynder library. At some point, I'll have to upload it. If things are breaking, just change things until it works.