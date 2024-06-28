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

#prompt for ipadapter interpolation
prompt_text_interpolation = """
{
  "3": {
    "inputs": {
      "seed": 4244721073,
      "steps": 4,
      "cfg": 1.3,
      "sampler_name": "dpmpp_sde",
      "scheduler": "karras",
      "denoise": 0.8,
      "model": [
        "567",
        0
      ],
      "positive": [
        "133",
        0
      ],
      "negative": [
        "138",
        0
      ],
      "latent_image": [
        "654",
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
      "ckpt_name": "SDXL\\lightning turbo\\juggernautXL_v9Rdphoto2Lightning.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
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
  "133": {
    "inputs": {
      "text": "",
      "clip": [
        "367",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "138": {
    "inputs": {
      "text": "",
      "clip": [
        "367",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "367": {
    "inputs": {
      "stop_at_clip_layer": -2,
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPSetLastLayer",
    "_meta": {
      "title": "CLIP Set Last Layer"
    }
  },
  "411": {
    "inputs": {
      "image": "frog.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load end img"
    }
  },
  "425": {
    "inputs": {
      "image": "fish.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load start img"
    }
  },
  "427": {
    "inputs": {
      "image": "dummy.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "559": {
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
  "567": {
    "inputs": {
      "weight": 1,
      "weight_type": "original",
      "start_at": 0,
      "end_at": 1,
      "unfold_batch": false,
      "ipadapter": [
        "570",
        0
      ],
      "embeds": [
        "569",
        0
      ],
      "model": [
        "4",
        0
      ]
    },
    "class_type": "IPAdapterApplyEncoded",
    "_meta": {
      "title": "Apply IPAdapter from Encoded"
    }
  },
  "569": {
    "inputs": {
      "ipadapter_plus": false,
      "noise": 0.2,
      "weight_1": 0.5,
      "weight_2": 0.5,
      "weight_3": 0,
      "weight_4": 0,
      "clip_vision": [
        "571",
        0
      ],
      "image_1": [
        "425",
        0
      ],
      "image_2": [
        "411",
        0
      ],
      "image_3": [
        "427",
        0
      ],
      "image_4": [
        "572",
        0
      ]
    },
    "class_type": "IPAdapterEncoder",
    "_meta": {
      "title": "Encode IPAdapter Image"
    }
  },
  "570": {
    "inputs": {
      "ipadapter_file": "ip-adapter_sdxl_vit-h.safetensors"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "Load IPAdapter Model"
    }
  },
  "571": {
    "inputs": {
      "clip_name": "small.safetensors"
    },
    "class_type": "CLIPVisionLoader",
    "_meta": {
      "title": "Load CLIP Vision"
    }
  },
  "572": {
    "inputs": {
      "image": "dummy.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "651": {
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
  "652": {
    "inputs": {
      "image": "dummy.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load first img"
    }
  },
  "653": {
    "inputs": {
      "pixels": [
        "652",
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
  "654": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "width": 1024,
      "height": 1024,
      "crop": "disabled",
      "samples": [
        "653",
        0
      ]
    },
    "class_type": "LatentUpscale",
    "_meta": {
      "title": "Upscale Latent"
    }
  }
}
"""

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

def image_interpolation(steps, start, end, image1, image2, image_to_be_processed):
    prompt = json.loads(prompt_text_interpolation)
    prompt["425"]["inputs"]["image"] = image1 + ".png"
    prompt["411"]["inputs"]["image"] = image2 + ".png"

    '''
    this is for generating series of pictures that involves interpolated value of smthing
    @steps: how many steps interpolation has
    @altered_value: which element is modified?
       
    '''
    for step in range(1,1+steps):
        new_value = start + (end-start)/steps*step
        prompt["569"]["inputs"]["weight_1"] = new_value
        new_value = start + (end-start)/steps*(steps-step)
        prompt["569"]["inputs"]["weight_2"] = new_value
        queue_prompt(prompt)
        image_to_be_processed = image_watch(image_to_be_processed)
        print(image_to_be_processed)

def image_zoom(steps, scale_by,prompt_text, x = 20,y = 11):
    """zooms in one particular direction
    @steps: how many steps of this """
    global generated_image
    prompt = json.loads(prompt_text_zoom) 
    prompt["3"]["inputs"]["denoise"] = denoise
    prompt["15"]["inputs"]["image"] = "processed.png"
    prompt["6"]["inputs"]["text"] = prompt_text
    prompt["13"]["inputs"]["x"] = x  #34 for centered zoom at 1.05 and [1344,768]
    prompt["13"]["inputs"]["y"] = y  #19 for centered zoom
    prompt["14"]["inputs"]["scale_by"] = scale_by
    steps_done = 0
    while(steps>steps_done):
        steps_done +=1
        prompt["3"]["inputs"]["seed"] += 1 
        queue_prompt(prompt)
        generated_image = image_watch(generated_image)
        copy_and_rename_image(generated_image, path_to_load_image, "processed.png")

def image_zoom_n_interpolation(steps, scale_by,prompt_text_start, prompt_text_end, x = 20,y = 11):
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
    prompt["15"]["inputs"]["image"] = "processed.png"
    prompt["6"]["inputs"]["text"] = prompt_text_start
    prompt["19"]["inputs"]["text"] = prompt_text_end
    prompt["13"]["inputs"]["x"] = x  #34 for centered zoom at 1.05 and [1344,768]
    prompt["13"]["inputs"]["y"] = y  #19 for centered zoom
    prompt["14"]["inputs"]["scale_by"] = scale_by
    steps_done = 0
    while(steps>steps_done):
        steps_done +=1
        prompt["3"]["inputs"]["seed"] += 1 
        prompt["21"]["inputs"]["conditioning_to_strength"] = steps_done/steps
        queue_prompt(prompt)
        generated_image = image_watch(generated_image)
        copy_and_rename_image(generated_image, path_to_load_image, "processed.png")


denoise = 0.45 #denoise of latent image
prompt_text = "hydrogen atom. 3d render"
generated_image = image_watch
image_zoom(99, 1.03, prompt_text)
p1 = prompt_text
p2 = "steel reactor for hydrogenation. 3d render"
image_zoom_n_interpolation(180,1.03,p1,p2)

image_zoom(300, 1.03, p2)

p1 = p2
p2 = "large sun. closeup telescope image"
image_zoom_n_interpolation(180,1.03,p1,p2)

image_zoom(320, 1.03, p2)

p1 = p2
p2 = "explosion in empty space"
image_zoom_n_interpolation(120,1.03,p1,p2)

p1 = p2
p2 = "water sphere. 3d render"
image_zoom_n_interpolation(120,1.03,p1,p2)

image_zoom(320, 1.03, p2)
