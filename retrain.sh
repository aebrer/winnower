python retrain.py --bottleneck_dir=tf_files/bottlenecks \
    --how_many_training_steps=20000 \
    --model_dir=models/ \
    --learning_rate=0.0001 \
    --summaries_dir=tf_files/training_summaries \
    --output_labels=tf_files/retrained_labels.txt \
    --output_graph=inception_two_class_model.pb \
    --image_dir=/home/andrew/winnower/ranked_sets \
    --print_misclassified_test_images

