import cv2
import numpy as np
from pathlib import Path

def create_test_video():
    # Create directories if they don't exist
    test_dir = Path("test_videos")
    test_dir.mkdir(exist_ok=True)
    
    # Video parameters
    width, height = 640, 480
    fps = 30
    duration = 5  # seconds
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(test_dir / "test.mp4"), fourcc, fps, (width, height))
    
    # Generate frames
    for i in range(total_frames):
        # Create a frame with a moving color gradient
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add a moving gradient
        gradient = np.linspace(0, 255, width, dtype=np.uint8)
        gradient = np.tile(gradient, (height, 1))
        frame[:, :, 0] = gradient  # Blue channel
        frame[:, :, 1] = (gradient + i * 2) % 256  # Green channel
        frame[:, :, 2] = (gradient + i * 4) % 256  # Red channel
        
        # Add some text
        cv2.putText(frame, f"Frame {i}", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"Test video created at: {test_dir / 'test.mp4'}")

if __name__ == "__main__":
    create_test_video() 