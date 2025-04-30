from project.celery import app
import cv2
import os
from pathlib import Path

@app.task(bind=True)
def process_video(self, video_path, output_path):
    """
    Process a video file and save the processed version.
    Args:
        video_path (str): Path to the input video file
        output_path (str): Path where the processed video will be saved
    """
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {
                'status': 'error',
                'message': f'Could not open video file: {video_path}',
                'input_path': video_path
            }
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame (example: convert to grayscale)
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
            
            # Write the processed frame
            out.write(processed_frame)
            frame_count += 1
            
            # Update task state
            self.update_state(state='PROGRESS',
                            meta={'current': frame_count, 'total': 100})
        
        # Release everything
        cap.release()
        out.release()
        
        return {
            'status': 'success',
            'message': f'Video processed and saved to {output_path}',
            'input_path': video_path,
            'output_path': output_path,
            'frames_processed': frame_count
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'input_path': video_path
        }

@app.task(bind=True)
def extract_frames(self, video_path, output_dir, frame_interval=1):
    """
    Extract frames from a video at specified intervals.
    Args:
        video_path (str): Path to the input video file
        output_dir (str): Directory where frames will be saved
        frame_interval (int): Extract every Nth frame
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {
                'status': 'error',
                'message': f'Could not open video file: {video_path}',
                'input_path': video_path
            }
            
        frame_count = 0
        extracted_count = 0
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f'frame_{frame_count:06d}.jpg')
                cv2.imwrite(frame_path, frame)
                extracted_count += 1
                
                # Update task state
                self.update_state(state='PROGRESS',
                                meta={'current': frame_count, 'total': 100})
                
            frame_count += 1
            
        cap.release()
        
        return {
            'status': 'success',
            'message': f'Extracted {extracted_count} frames to {output_dir}',
            'input_path': video_path,
            'output_dir': output_dir,
            'total_frames': frame_count,
            'extracted_frames': extracted_count
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'input_path': video_path
        }

