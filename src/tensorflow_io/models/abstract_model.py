import tfjs_graph_converter.api as tfjs_api

class AbstractModel:
    def __init__(self, model_path, segment_logits_index, part_heatmaps_index, heatmaps_index):
        self.model_path = model_path

        self.segment_logits_index = segment_logits_index
        self.part_heatmaps_index = part_heatmaps_index
        self.heatmaps_index = heatmaps_index

        self.graph = tfjs_api.load_graph_model(self.model_path)

    def preprocessing(self, frame):
        return frame

    def get_tensor_outputs(self, results):
        segment_logits = results[self.segment_logits_index]
        part_heatmaps = results[self.part_heatmaps_index]
        heatmaps = results[self.heatmaps_index]
        return segment_logits, part_heatmaps, heatmaps