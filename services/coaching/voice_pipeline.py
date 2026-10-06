import time
import streamlit as st

class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)

            if depth == "TOO HIGH":
                return "The user's squat is not deep enough - knees are not bending sufficiently."

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return "The user is leaning too far forward during the squat."

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment","")
            hip_status = metrics.get("hip_status", "")

            if alignment == "Poor Form":
                return "The user's body is not straight during the push-up."

            if hip_status == "SAGGING":
                return "The user's hips are sagging down during push-up."

            if hip_status == "PIKED UP":
                return "The user's hips are too high - lower them to form a straight line."

        elif exercise == "Bicep Curl (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")

            if swing == "SWINGING":
                return "The user is swinging their torso during the curl - keep the body still."

            if shoulder == "ELBOW DRIFTING":
                return "The user's elbow is drifting away from their side during the curl."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")
            extension = metrics.get("extension_status", "")

            if back_arch == "EXCESSIVE ARCH":
                return "The user is arching their lower back excessively during the press."

            if back_arch == "SLIGHT ARCH":
                return "Slight back arch detected - encourage user to brace their core."

            if extension == "NEARLY EXTENDED":
                return "You are not fully extending your arms at the top. Press a little higher."

        elif exercise == "Lunges":
            balance =metrics.get("balance_status", "")

            if balance == "OFF BALANCE":
                return "The user is losing balance during the lunge - feet should be hip width"


        return None

    def process_event(self, event, exercise, metrics):
        print("=" * 50)
        print("process_event CALLED")
        print("Event:", event)
        print("Exercise:", exercise)
        print("Metrics:", metrics)

        issue = self._find_form_issue(exercise, metrics)
        print("Detected Issue:", issue)

        now = time.time()

        is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

        if not is_major_issue:
            if not issue:
                print("Returning None (No issue)")
                return None

            if now - self.last_spoken_at < 5:
                print("Returning None (Cooldown)")
                return None

        text = self.llm.give_feedback(event, issue)
        print("LLM Response:", text)

        voice = self.tts.speak(text)
        print("Voice Generated:", voice is not None)

        self.last_spoken_at = now

        print("Returning voice + text")
        print("=" * 50)

        return voice, text

def autoplay_audio(audio_bytes):
    if not audio_bytes:
        return

    st.markdown("<style>[data-testid='stAudio'] {display: none;}</style>",unsafe_allow_html=True)

    st.audio(audio_bytes, format = "audio/mp3", autoplay = True)

