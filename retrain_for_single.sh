python retrain.py --bottleneck_dir=tf_files/bottlenecks \
    --how_many_training_steps=30000 \
    --model_dir=models/ \
    --learning_rate=0.005 \
    --summaries_dir=tf_files/training_summaries \
    --output_labels=tf_files/retrained_labels.txt \
    --output_graph=inception_two_class_model_single.pb \
    --image_dir=/home/andrew/winnower/ranked_single_images \
    --print_misclassified_test_images \
    --testing_percentage=5 \
    --validation_percentage=15 \
    --validation_batch_size=75

