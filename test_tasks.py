from project.tasks import process_video, extract_frames
import os
from pathlib import Path

def main():
    # Create test directories
    input_dir = Path("test_videos")
    output_dir = Path("processed_videos")
    frames_dir = Path("extracted_frames")
    
    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    frames_dir.mkdir(exist_ok=True)
    
    # Example video paths
    input_video = str(input_dir / "test.mp4")  # Replace with your actual video file
    processed_video = str(output_dir / "processed_test.mp4")
    frames_output = str(frames_dir / "test_frames")
    
    print("Starting video processing tasks...")
    
    # Example 1: Process video (convert to grayscale)
    print("\nProcessing video...")
    result = process_video.delay(input_video, processed_video)
    print(f"Task ID: {result.id}")
    print("Waiting for task to complete...")
    task_result = result.get(timeout=300)  # Wait up to 5 minutes
    print(f"Task result: {task_result}")
    
    # Example 2: Extract frames
    print("\nExtracting frames...")
    result = extract_frames.delay(input_video, frames_output, frame_interval=30)
    print(f"Task ID: {result.id}")
    print("Waiting for task to complete...")
    task_result = result.get(timeout=300)  # Wait up to 5 minutes
    print(f"Task result: {task_result}")

if __name__ == "__main__":
    main() 