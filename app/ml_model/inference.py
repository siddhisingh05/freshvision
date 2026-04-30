import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F

# ===== CONFIG =====
CONF_THRESHOLD = 0.75  # adjust if needed

# ===== DEVICE =====
device = torch.device("cpu")

# ===== CLASSES =====
classes = [
    'freshapples', 'freshbanana', 'freshoranges',
    'rottenapples', 'rottenbanana', 'rottenoranges'
]

# ===== MODEL =====
model = resnet18(weights=ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, 6)

model.load_state_dict(torch.load("app/ml_model/best_model.pth", map_location=device))
model.eval()

# ===== TRANSFORM =====
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ===== PREDICTION FUNCTION =====
def predict_image(image: Image.Image):
    image = image.convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probs = F.softmax(outputs, dim=1)[0]

    best_idx = torch.argmax(probs).item()
    confidence = probs[best_idx].item()
    label = classes[best_idx]

    # 🚨 UNKNOWN DETECTION (MAIN FIX)
    if confidence < CONF_THRESHOLD:
        return {
            "fruit": "Unknown",
            "condition": "Uncertain",
            "confidence": round(confidence * 100, 2)
        }

    # ✅ NORMAL CASE
    condition = "Fresh" if "fresh" in label else "Rotten"
    fruit = label.replace("fresh", "").replace("rotten", "")

    return {
        "fruit": fruit.capitalize(),
        "condition": condition,
        "confidence": round(confidence * 100, 2)
    }