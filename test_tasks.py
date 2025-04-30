from project.tasks import process_video, extract_frames
import os
from pathlib import Path
import time

def print_task_progress(task):
    """Print task progress updates"""
    try:
        while not task.ready():
            if task.info:
                print(f"Progress: {task.info.get('current', 0)}%")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTask interrupted by user")
        return

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
    input_video = str(input_dir / "test.mp4")
    processed_video = str(output_dir / "processed_test.mp4")
    frames_output = str(frames_dir / "test_frames")
    
    print("Starting video processing tasks...")
    
    try:
        # Example 1: Process video (convert to grayscale)
        print("\nProcessing video...")
        result = process_video.delay(input_video, processed_video)
        print(f"Task ID: {result.id}")
        print("Waiting for task to complete...")
        print_task_progress(result)
        task_result = result.get(timeout=300)  # Wait up to 5 minutes
        print(f"Task result: {task_result}")
        
        # Example 2: Extract frames
        print("\nExtracting frames...")
        result = extract_frames.delay(input_video, frames_output, frame_interval=30)
        print(f"Task ID: {result.id}")
        print("Waiting for task to complete...")
        print_task_progress(result)
        task_result = result.get(timeout=300)  # Wait up to 5 minutes
        print(f"Task result: {task_result}")
        
    except Exception as e:
        print(f"Error during task execution: {e}")

if __name__ == "__main__":
    main() 