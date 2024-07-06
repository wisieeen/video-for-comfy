#keep at least single image in output folder of comfyui, place in input folder file named "processed.png" as initial image

import json
from urllib import request, parse
import random
import glob
import os
import time
from shutil import copy2

path_to_save_image = "E:\\ComfyUI_windows\\ComfyUI\\output\\"
path_to_load_image = "E:\\ComfyUI_windows\\ComfyUI\\input\\"
generated_image = "ComfyUI_00001_.png"


#it infinitely zooms in chosen direction
prompt_text_zoom = """{
  "3": {
    "inputs": {
      "seed": 173159221572310,
      "steps": 4,
      "cfg": 2,
      "sampler_name": "euler_ancestral",
      "scheduler": "sgm_uniform",
      "denoise": 0.05,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "dreamshaperXL_lightningDPMSDE.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "interdimensional portal",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "10": {
    "inputs": {
      "images": [
        "8",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "13",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "13": {
    "inputs": {
      "width": 1344,
      "height": 768,
      "x": 34,
      "y": 19,
      "image": [
        "14",
        0
      ]
    },
    "class_type": "ImageCrop",
    "_meta": {
      "title": "ImageCrop"
    }
  },
  "14": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 1.05,
      "image": [
        "15",
        0
      ]
    },
    "class_type": "ImageScaleBy",
    "_meta": {
      "title": "Upscale Image By"
    }
  },
  "15": {
    "inputs": {
      "image": "ComfyUI_temp_phrmn_00128_.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "18": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}"""

#it interpolates between prompts and zooms
prompt_interpolation = """
{
  "3": {
    "inputs": {
      "seed": 173159221580066,
      "steps": 4,
      "cfg": 2,
      "sampler_name": "euler_ancestral",
      "scheduler": "sgm_uniform",
      "denoise": 0.45,
      "model": [
        "4",
        0
      ],
      "positive": [
        "21",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "dreamshaperXL_lightningDPMSDE.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "diamond in coal wall under high pressure and temperature deep underground. 3d render",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "10": {
    "inputs": {
      "images": [
        "8",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "13",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "13": {
    "inputs": {
      "width": 1344,
      "height": 768,
      "x": 20,
      "y": 11,
      "image": [
        "14",
        0
      ]
    },
    "class_type": "ImageCrop",
    "_meta": {
      "title": "ImageCrop"
    }
  },
  "14": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 1.03,
      "image": [
        "15",
        0
      ]
    },
    "class_type": "ImageScaleBy",
    "_meta": {
      "title": "Upscale Image By"
    }
  },
  "15": {
    "inputs": {
      "image": "processed.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "18": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "19": {
    "inputs": {
      "text": "diamond in saw blade disc cutting toughest materials. 3d render",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "21": {
    "inputs": {
      "conditioning_to_strength": 0,
      "conditioning_to": [
        "19",
        0
      ],
      "conditioning_from": [
        "6",
        0
      ]
    },
    "class_type": "ConditioningAverage",
    "_meta": {
      "title": "ConditioningAverage"
    }
  }
}
"""

prompt_lora_embed_interpolation = """{
  "3": {
    "inputs": {
      "seed": 1034983277368647,
      "steps": 6,
      "cfg": 1.5,
      "sampler_name": "euler_ancestral",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "57",
        0
      ],
      "positive": [
        "21",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "89",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "mklanXXXNSFWVersion_mklan19.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "drone_view, analog photography, black hair, car materace backseat, vaginal sex",
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark, empty, boring, NSFW, nude",
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "75",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "14": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "scale_by": 1.03,
      "image": [
        "15",
        0
      ]
    },
    "class_type": "ImageScaleBy",
    "_meta": {
      "title": "Upscale Image By"
    }
  },
  "15": {
    "inputs": {
      "image": "ComfyUI_temp_tjtgh_00006_.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "19": {
    "inputs": {
      "text": "drone_view, analog photography, black hair, car materace backseat, vaginal sex",
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "21": {
    "inputs": {
      "conditioning_to_strength": 0,
      "conditioning_to": [
        "19",
        0
      ],
      "conditioning_from": [
        "6",
        0
      ]
    },
    "class_type": "ConditioningAverage",
    "_meta": {
      "title": "ConditioningAverage"
    }
  },
  "22": {
    "inputs": {
      "lora_name": {
        "content": "VnC_beta.safetensors",
        "image": null
      },
      "strength_model": 0.8,
      "strength_clip": 1,
      "example": "[none]",
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader|pysssss",
    "_meta": {
      "title": "Lora Loader 🐍"
    }
  },
  "28": {
    "inputs": {
      "images": [
        "29",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "29": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "30": {
    "inputs": {
      "lora_name": {
        "content": "VnC_beta.safetensors",
        "image": null
      },
      "strength_model": 0,
      "strength_clip": 0,
      "example": "[none]",
      "model": [
        "22",
        0
      ],
      "clip": [
        "22",
        1
      ]
    },
    "class_type": "LoraLoader|pysssss",
    "_meta": {
      "title": "Lora Loader 🐍"
    }
  },
  "33": {
    "inputs": {
      "ipadapter_file": "ip-adapter_sdxl_vit-h.safetensors"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "Load IPAdapter Model"
    }
  },
  "34": {
    "inputs": {
      "weight": 0.9,
      "weight_type": "channel penalty",
      "start_at": 0.3,
      "end_at": 1,
      "unfold_batch": false,
      "ipadapter": [
        "33",
        0
      ],
      "embeds": [
        "35",
        0
      ],
      "model": [
        "30",
        0
      ]
    },
    "class_type": "IPAdapterApplyEncoded",
    "_meta": {
      "title": "Apply IPAdapter from Encoded"
    }
  },
  "35": {
    "inputs": {
      "ipadapter_plus": false,
      "noise": 0.3,
      "weight_1": 0.9,
      "weight_2": 0,
      "weight_3": 0.8,
      "weight_4": 0,
      "clip_vision": [
        "36",
        0
      ],
      "image_1": [
        "37",
        0
      ],
      "image_2": [
        "38",
        0
      ],
      "image_3": [
        "39",
        0
      ],
      "image_4": [
        "40",
        0
      ]
    },
    "class_type": "IPAdapterEncoder",
    "_meta": {
      "title": "Encode IPAdapter Image"
    }
  },
  "36": {
    "inputs": {
      "clip_name": "small.safetensors"
    },
    "class_type": "CLIPVisionLoader",
    "_meta": {
      "title": "Load CLIP Vision"
    }
  },
  "37": {
    "inputs": {
      "image": "sumin1.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "38": {
    "inputs": {
      "image": "mmexport1586689643614.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "39": {
    "inputs": {
      "image": "sumin4.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "40": {
    "inputs": {
      "image": "sumin3.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "54": {
    "inputs": {
      "width": 1344,
      "height": 768,
      "x": 25,
      "y": 11,
      "image": [
        "14",
        0
      ]
    },
    "class_type": "ImageCrop",
    "_meta": {
      "title": "ImageCrop"
    }
  },
  "56": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "aspect_ratio": "3:4 portrait 896x1152",
      "swap_dimensions": "Off",
      "upscale_factor": 1,
      "batch_size": 1
    },
    "class_type": "CR SDXL Aspect Ratio",
    "_meta": {
      "title": "🔳 CR SDXL Aspect Ratio"
    }
  },
  "57": {
    "inputs": {
      "weight": 0.8,
      "weight_type": "channel penalty",
      "start_at": 0,
      "end_at": 0.2,
      "unfold_batch": false,
      "ipadapter": [
        "33",
        0
      ],
      "embeds": [
        "58",
        0
      ],
      "model": [
        "34",
        0
      ]
    },
    "class_type": "IPAdapterApplyEncoded",
    "_meta": {
      "title": "Apply IPAdapter from Encoded"
    }
  },
  "58": {
    "inputs": {
      "ipadapter_plus": false,
      "noise": 0.3,
      "weight_1": 1,
      "weight_2": 0,
      "weight_3": 0,
      "weight_4": 0,
      "clip_vision": [
        "36",
        0
      ],
      "image_1": [
        "60",
        0
      ],
      "image_2": [
        "81",
        0
      ],
      "image_3": [
        "61",
        0
      ],
      "image_4": [
        "62",
        0
      ]
    },
    "class_type": "IPAdapterEncoder",
    "_meta": {
      "title": "Encode IPAdapter Image"
    }
  },
  "60": {
    "inputs": {
      "image": "ComfyUI_temp_yktih_00001_.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "61": {
    "inputs": {
      "image": "sumin4.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "62": {
    "inputs": {
      "image": "night.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "69": {
    "inputs": {
      "left": 16,
      "top": 8,
      "right": 16,
      "bottom": 8,
      "feathering": 90,
      "image": [
        "15",
        0
      ]
    },
    "class_type": "ImagePadForOutpaint",
    "_meta": {
      "title": "Pad Image for Outpainting"
    }
  },
  "70": {
    "inputs": {
      "enabled": true,
      "swap_model": "inswapper_128.onnx",
      "facedetection": "retinaface_resnet50",
      "face_restore_model": "codeformer.pth",
      "face_restore_visibility": 1,
      "codeformer_weight": 0.5,
      "detect_gender_source": "no",
      "detect_gender_input": "no",
      "source_faces_index": "0",
      "input_faces_index": "0",
      "console_log_level": 1,
      "input_image": [
        "122",
        0
      ],
      "source_image": [
        "71",
        0
      ]
    },
    "class_type": "ReActorFaceSwap",
    "_meta": {
      "title": "ReActor - Fast Face Swap"
    }
  },
  "71": {
    "inputs": {
      "image": "sumin4.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "74": {
    "inputs": {
      "images": [
        "70",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "75": {
    "inputs": {
      "Input": 2,
      "image1": [
        "54",
        0
      ],
      "image2": [
        "106",
        0
      ]
    },
    "class_type": "CR Image Input Switch",
    "_meta": {
      "title": "🔀 CR Image Input Switch"
    }
  },
  "80": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "70",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "81": {
    "inputs": {
      "image": "ComfyUI_temp_yktih_00001_.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "85": {
    "inputs": {
      "samples": [
        "12",
        0
      ],
      "mask": [
        "95",
        0
      ]
    },
    "class_type": "SetLatentNoiseMask",
    "_meta": {
      "title": "Set Latent Noise Mask"
    }
  },
  "88": {
    "inputs": {
      "images": [
        "107",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "89": {
    "inputs": {
      "Input": 2,
      "latent1": [
        "12",
        0
      ],
      "latent2": [
        "85",
        0
      ]
    },
    "class_type": "CR Latent Input Switch",
    "_meta": {
      "title": "🔀 CR Latent Input Switch"
    }
  },
  "90": {
    "inputs": {
      "upscale_method": "bicubic",
      "width": 1344,
      "height": 768,
      "crop": "disabled"
    },
    "class_type": "LatentUpscale",
    "_meta": {
      "title": "Upscale Latent"
    }
  },
  "95": {
    "inputs": {
      "channel": "blue",
      "image": [
        "100",
        0
      ]
    },
    "class_type": "ImageToMask",
    "_meta": {
      "title": "Convert Image to Mask"
    }
  },
  "99": {
    "inputs": {
      "width": 1344,
      "height": 768,
      "batch_size": 1,
      "color": 0
    },
    "class_type": "EmptyImage",
    "_meta": {
      "title": "EmptyImage"
    }
  },
  "100": {
    "inputs": {
      "blend_factor": 1,
      "blend_mode": "screen",
      "image1": [
        "99",
        0
      ],
      "image2": [
        "102",
        0
      ]
    },
    "class_type": "ImageBlend",
    "_meta": {
      "title": "ImageBlend"
    }
  },
  "101": {
    "inputs": {
      "mask": [
        "69",
        1
      ]
    },
    "class_type": "MaskToImage",
    "_meta": {
      "title": "Convert Mask to Image"
    }
  },
  "102": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "width": 1344,
      "height": 768,
      "crop": "disabled",
      "image": [
        "101",
        0
      ]
    },
    "class_type": "ImageScale",
    "_meta": {
      "title": "Upscale Image"
    }
  },
  "103": {
    "inputs": {
      "blend_factor": 1,
      "blend_mode": "screen",
      "image1": [
        "100",
        0
      ],
      "image2": [
        "75",
        0
      ]
    },
    "class_type": "ImageBlend",
    "_meta": {
      "title": "ImageBlend"
    }
  },
  "104": {
    "inputs": {
      "samples": [
        "12",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "106": {
    "inputs": {
      "upscale_method": "bilinear",
      "width": 1344,
      "height": 768,
      "crop": "disabled",
      "image": [
        "69",
        0
      ]
    },
    "class_type": "ImageScale",
    "_meta": {
      "title": "Upscale Image"
    }
  },
  "107": {
    "inputs": {
      "mask": [
        "95",
        0
      ]
    },
    "class_type": "MaskToImage",
    "_meta": {
      "title": "Convert Mask to Image"
    }
  },
  "113": {
    "inputs": {
      "images": [
        "104",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "114": {
    "inputs": {
      "samples": [
        "89",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "115": {
    "inputs": {
      "images": [
        "114",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "116": {
    "inputs": {
      "images": [
        "15",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "118": {
    "inputs": {
      "x": 0,
      "y": 0,
      "resize_source": false,
      "destination": [
        "106",
        0
      ],
      "source": [
        "29",
        0
      ],
      "mask": [
        "121",
        0
      ]
    },
    "class_type": "ImageCompositeMasked",
    "_meta": {
      "title": "ImageCompositeMasked"
    }
  },
  "119": {
    "inputs": {
      "images": [
        "122",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "121": {
    "inputs": {
      "channel": "blue",
      "image": [
        "102",
        0
      ]
    },
    "class_type": "ImageToMask",
    "_meta": {
      "title": "Convert Image to Mask"
    }
  },
  "122": {
    "inputs": {
      "Input": 2,
      "image1": [
        "29",
        0
      ],
      "image2": [
        "127",
        0
      ]
    },
    "class_type": "CR Image Input Switch",
    "_meta": {
      "title": "🔀 CR Image Input Switch"
    }
  },
  "123": {
    "inputs": {
      "seed": 561284598450496,
      "steps": 6,
      "cfg": 1.5,
      "sampler_name": "dpm_2_ancestral",
      "scheduler": "normal",
      "denoise": 0.43,
      "model": [
        "57",
        0
      ],
      "positive": [
        "21",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "124",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "124": {
    "inputs": {
      "pixels": [
        "118",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "126": {
    "inputs": {
      "images": [
        "127",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "127": {
    "inputs": {
      "samples": [
        "123",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  }
}"""

embed_IPA_lora_out = 'E:\\sagAI\\video for comfy\\video-for-comfy\\embed IPA 2lora outpaint.json'


embed_IPA_lora_in = 'E:\\sagAI\\video for comfy\\video-for-comfy\\embed IPA 2lora zoom.json'
       

def copy_and_rename_image(source_name, destination_directory, new_name):
    """Copies an image file from source to destination and renames it.
    @source_name: path to image to be copied
    @destination_directory: folder path of destination
    @new_name: final name of copied file. include desired extension
    """
    time.sleep(.2) #without sleep file may be processed while saving or coping not finished and break script
    d = copy2(source_name, destination_directory)
    os.unlink('E:\\ComfyUI_windows\\ComfyUI\\input\\processed.png')
    time.sleep(.2)
    os.rename(d, destination_directory + new_name)
    time.sleep(.1)

def queue_prompt(prompt):
    """sends prompt to comfyUI"""
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

def image_watch(latest_file):
    '''
    function that waits until new file appears in folder
    returns name ot this file
    @latest_file: last generated file
    '''
    maybe_latest_file = latest_file

    while(latest_file == maybe_latest_file):
        list_of_files = glob.glob(path_to_save_image + "*.png") # * means all if need specific format then *.csv
        maybe_latest_file = max(list_of_files, key=os.path.getctime)
        time.sleep(.1)

    latest_file = maybe_latest_file 
    print("latest file:")
    print(latest_file)   
    return(latest_file)

def image_zoom(steps, scale_by,prompt_text, x = 17,y = 11):
    """zooms in one particular direction
    @steps: how many steps of this """
    global generated_image
    prompt = json.loads(prompt_text_zoom) 
    prompt["3"]["inputs"]["denoise"] = denoise
    prompt["15"]["inputs"]["image"] = "processed.png"
    prompt["6"]["inputs"]["text"] = prompt_text
    prompt["7"]["inputs"]["text"] = "text, watermark, empty, boring, NSFW, nude" #negatives
    prompt["13"]["inputs"]["x"] = x  #34 for centered zoom at 1.05 and [1344,768]
    prompt["13"]["inputs"]["y"] = y  #19 for centered zoom
    prompt["14"]["inputs"]["scale_by"] = scale_by
    steps_done = 0
    while(steps>steps_done):
        steps_done +=1
        if (steps_done % 30) ==0:
            prompt["3"]["inputs"]["seed"] += 1 
        prompt["3"]["inputs"]["denoise"] = (denoise - (0.6/(1 + (steps_done % 30))))
        queue_prompt(prompt)
        generated_image = image_watch(generated_image)
        copy_and_rename_image(generated_image, path_to_load_image, "processed.png")

def image_zoom_n_interpolation(steps, scale_by,prompt_text_start, prompt_text_end, x = 17,y = 11):
    """zooms in one particular direction
    @steps: how many steps of this stransition
    @scale_by: scale factor
    @prompt_text_start: prompt to start with
    @prompt_text_end: prompt to end with
    @x: cut pixels to left
    @y: cut pixels from top """

    global generated_image
    prompt = json.loads(prompt_interpolation) 
    prompt["3"]["inputs"]["denoise"] = denoise
    prompt["3"]["inputs"]["cfg"] = 1
    prompt["15"]["inputs"]["image"] = "processed.png"
    prompt["6"]["inputs"]["text"] = prompt_text_start
    prompt["19"]["inputs"]["text"] = prompt_text_end
    prompt["7"]["inputs"]["text"] = "text, watermark, empty, boring, NSFW, nude" #negatives
    prompt["13"]["inputs"]["x"] = x  #34 for centered zoom at 1.05 and [1344,768]
    prompt["13"]["inputs"]["y"] = y  #19 for centered zoom
    prompt["14"]["inputs"]["scale_by"] = scale_by

    steps_done = 0
    while(steps>steps_done):
        steps_done +=1
        if (steps_done % 30) ==0:
            prompt["3"]["inputs"]["seed"] += 1 
        prompt["3"]["inputs"]["denoise"] = (denoise - (0.6/(1 + (steps_done % 30))))
        prompt["21"]["inputs"]["conditioning_to_strength"] = steps_done/steps
        print("steps done: %i, denoise: %f, conditioning: %f" % (steps_done, (denoise - (0.6/(1 + (steps_done % 30)))),steps_done/steps))
        queue_prompt(prompt)
        generated_image = image_watch(generated_image)
        copy_and_rename_image(generated_image, path_to_load_image, "processed.png")

def prompt_prepare(pr, scale_by,prompt_text_start, prompt_text_end, prompt_text_start_n, x = 17,y = 11):
    global generated_image
    with open(pr) as f:
        prompt = json.load(f)
    wi = 1344
    he = 768    
    #prompt["4"]["inputs"]["ckpt_name"] ="mklanXXXNSFWVersion_mklan19.safetensors"
    prompt["4"]["inputs"]["ckpt_name"] ="dreamshaperXL_lightningDPMSDE.safetensors"
    prompt["123"]["inputs"]["denoise"] = denoise
    prompt["123"]["inputs"]["cfg"] = 1.5
    prompt["123"]["inputs"]["sampler_name"] = "euler_ancestral"
    prompt["123"]["inputs"]["scheduler"] = "sgm_uniform"
    prompt["15"]["inputs"]["image"] = "processed.png"
    prompt["6"]["inputs"]["text"] = prompt_text_start
    prompt["19"]["inputs"]["text"] = prompt_text_end
    prompt["7"]["inputs"]["text"] = prompt_text_start_n #negatives
    prompt["80"]["inputs"]["images"] = ["70",0] #save without watermark 
    #prompt["80"]["inputs"]["images"] = ["128",0] #with watermark 
    try:
        prompt["37"]["inputs"]["image"] = "sumin4.png"
        prompt["38"]["inputs"]["image"] = "sumin4.png"
        prompt["39"]["inputs"]["image"] = "sumin4.png"
        prompt["40"]["inputs"]["image"] = "sumin4.png"
        prompt["35"]["inputs"]["weight_1"] =1
        prompt["35"]["inputs"]["weight_2"] =0
        prompt["35"]["inputs"]["weight_3"] =0
        prompt["35"]["inputs"]["weight_4"] =0
    except:
        print("no embeding IPA")

    try:
        prompt["128"]["inputs"]["text"] = str(denoise) #"@ wisieeen293"
    except:
        print("no watermark")

    try:
        prompt["71"]["inputs"]["image"] = "sumin4.png" #photo for ReActor
    except:
        print("no ReActor")

    try:
        prompt["57"]["inputs"]["weight"] = 0 #weight of position IPA
    except:
        print("no position IPA")

    try:
        prompt["69"]["inputs"]["left"] = 16
        prompt["69"]["inputs"]["right"] = 16
        prompt["69"]["inputs"]["top"] = 8
        prompt["69"]["inputs"]["bottom"] = 8
        prompt["69"]["inputs"]["feathering"] = 40
    except:
        print("no outpaint")
    
    try:
        prompt["102"]["inputs"]["width"] = wi
        prompt["102"]["inputs"]["height"] = he
        prompt["106"]["inputs"]["width"] = wi
        prompt["106"]["inputs"]["height"] = he
    except:
        print("missing scale node")

    try:
        prompt["90"]["inputs"]["width"] = wi
        prompt["90"]["inputs"]["height"] = he
        prompt["54"]["inputs"]["width"] = wi
        prompt["54"]["inputs"]["height"] = he
    except:
        print("missing scale node (but other)")
    
    try:
        prompt["54"]["inputs"]["x"] = x  #34 for centered zoom at 1.05 and [1344,768]
        prompt["54"]["inputs"]["y"] = y  #19 for centered zoom
        prompt["14"]["inputs"]["scale_by"] = scale_by
    except:
        print("no scale nodes available")
    
    return prompt

def image_lora_embed_reactor_interpolation(steps, scale_by,prompt_text_start, prompt_text_end, x = 25,y = 11):
    """zooms in one particular direction, then outpaints and repeats
    interpolates between prompts, contains IPadapter and 2 loras
    @steps: how many steps of this stransition
    @scale_by: scale factor
    @prompt_text_start: prompt to start with
    @prompt_text_end: prompt to end with
    @x: cut pixels to left
    @y: cut pixels from top """

    global generated_image
    prompt1 = prompt_prepare(embed_IPA_lora_out, scale_by,prompt_text_start, prompt_text_end, negative, x = x,y = y)
    prompt2 = prompt_prepare(embed_IPA_lora_in, scale_by,prompt_text_start, prompt_text_end, negative, x = x,y = y)
    pp = prompt1
    steps_done = 0
    cf_cycle = 30 #length of zooming in/out cycle
    while(steps>steps_done):
        steps_done +=1
        prompt1["21"]["inputs"]["conditioning_to_strength"] = steps_done/steps
        prompt2["21"]["inputs"]["conditioning_to_strength"] = steps_done/steps

        print("steps done: %i, denoise: %f, conditioning: %f" % (steps_done, (denoise - (0.6/(1 + (steps_done % 30)))),steps_done/steps))
        if (steps_done % 25) ==0:
            prompt1["123"]["inputs"]["seed"] += 1 
            prompt2["123"]["inputs"]["seed"] += 1

        if (steps_done%cf_cycle) ==0:
            print("prompt1 runs")
            pp = prompt1

        elif (steps_done%cf_cycle) ==20:
            print("prompt2 runs")
            pp = prompt2


        queue_prompt(pp)
        #prompt["3"]["inputs"]["denoise"] = (denoise - (0.6/(1 + (steps_done % 30))))
        generated_image = image_watch(generated_image)
        copy_and_rename_image(generated_image, path_to_load_image, "processed.png")


standard_steps = 90
scale_up_factor = 1.03
denoise = 0.9 #denoise of latent image

prompt_text = "analog photography, side view photo of girl sleeping, d_medium"
negative = "text, watermark, empty, naked, NSFW, boring, deformed body, additional limbs, missing limbs"
generated_image = image_watch(generated_image)
copy_and_rename_image(generated_image,path_to_load_image,"processed.png")
#image_zoom(99, 1.03, prompt_text)

while(True):
    p1 = prompt_text
    p2 = "analog photography, side view photo of female eating breakfast, d_medium"
    image_lora_embed_reactor_interpolation(standard_steps,scale_up_factor,prompt_text,p2)

    p1 = p2
    p2 = prompt_text
    image_lora_embed_reactor_interpolation(standard_steps,scale_up_factor,p1,p2)
    denoise -= 0.05

"""while(True):
    
    p2 = prompt_text

    p1 = p2
    p2 = "full_body, eye level, analog photography showing 10yo girl student sitting in school, 1990s, tracksuit uniform, short hair"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female student studying in library, reading book, glasses, 2000s"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    #image_zoom(320, 1.03, p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female student walking, sydney opera in background"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing girl sitting on boat in (New york city),  statue of liberty in background"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female sitting in office, looking through window, female using computer, (forbidden city in beijing seen from tall building:0.4)"
    image_lora_embed_interpolationn(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female walking down chinese village, casual outfit with backpack"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female scuba diving in thailand"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing female hiking in lowland coniferous forest, grass on floor"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing (european man) and chinese female standing together, happy faces, interracial couple, British man, german man, polish male, swedish boy "
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    p1 = p2
    p2 = "full_body, eye level, analog photography showing pregnant female, shopping mall"
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)

    image_zoom(120, 1.03, p2)

    p1 = p2
    p2 = prompt_text
    image_lora_embed_interpolation(standard_steps,scale_up_factor,p1,p2)"""