# ZED2i-Perception-RGB-only-
ZED 2i Stereo RGB acquisition, calibration, offline stereo matching (OpenCV), error analysis. Reusable front-end for Vision-Guided Planning &amp; Control of ASV.

- **Hardware:** ZED 2i (stereo RGB) on NTUAAVPC3 (Intel iGPU)
- **Software:** Ubuntu 24.04, ROS 2 Jazzy, OpenCV (offline stereo), Python
- **Outputs:** calibration YAML, rectified pairs, disparity/depth maps, error analysis tables/plots
- **ASV2.0 link:** same pipeline will be swapped to Basler cameras + GPU later

## Repo layout
- `calibration/` — chessboard images + `camchain.yaml`
- `stereo/` — OpenCV scripts for rectification, SGBM/BM, depth computation
- `scripts/` — rosbag record helpers, quick capture
- `docs/` — report notes and figures
- `results/` — plots/tables (keep small; large data goes to LFS or external storage)

## Quickstart
```bash
# Setup venv (optional)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Record RGB topics (example)
ros2 bag record -o ~/bags/zed2i_rgb \
  /zed2i/zed_node/left/image_rect_color \
  /zed2i/zed_node/right/image_rect_color \
  /zed2i/zed_node/left/camera_info \
  /zed2i/zed_node/right/camera_info

# Run offline stereo
python stereo/run_sgbm.py --left path/to/left.png --right path/to/right.png --calib calibration/camchain.yaml
