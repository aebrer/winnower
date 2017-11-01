python retrain.py \
  --bottleneck_dir=tf_files/bottlenecks \
  --how_many_training_steps=7000 \
  --model_dir=tf_files/models/ \
  --validation_batch_size=-1 \
  --learning_rate=0.0001 \
  --summaries_dir=tf_files/training_summaries/mobilenet_1.0_224 \
  --output_graph=tf_files/mobilenet_two_class.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture=mobilenet_1.0_224 \
  --image_dir=/home/andrew/winnower/ranked_sets \
  #--random_crop=5 --random_brightness=5 --random_scale=5


