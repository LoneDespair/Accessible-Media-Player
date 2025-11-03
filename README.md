# Accessible Media Player
An assistive technology for users with motor impairments. The user can control their music or video player (play, pause, or change volume) by making distinct facial gestures like turning your head, tilting, or opening their mouth.

## Requirements
- MediaPipe: for creating a face mesh
- KivyMD: for the ready-made video player
- FFPyPlayer: for playing videos
```
pip install mediapipe kivymd ffpyplayer
```

## Usage
```
python video_player.py
```
This video player is controlled by facial expressions and actions. A well-lit environment is recommended, though it can also work in moderately-lit surroundings. It plays the video when a face is detected, and pauses it when you look away or leave the computer. This feature can be disabled using the spacebar. To control the volume, tilt your head to the left or right. You can also rewind or seek forward the video by turning your head in the direction you want to move the playback position.
