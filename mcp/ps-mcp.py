# MIT License
#
# Copyright (c) 2025 Mike Chambers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from mcp.server.fastmcp import FastMCP, Image
from core import init, sendCommand, createCommand
from fonts import list_all_fonts_postscript
import numpy as np
import base64
import socket_client
import sys
import os

FONT_LIMIT = 1000 #max number of font names to return to AI

#logger.log(f"Python path: {sys.executable}")
#logger.log(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
#logger.log(f"Current working directory: {os.getcwd()}")
#logger.log(f"Sys.path: {sys.path}")


mcp_name = "Adobe Photoshop MCP Server"
mcp = FastMCP(mcp_name, log_level="ERROR")
# print(f"{mcp_name} running on stdio", file=sys.stderr)

APPLICATION = "photoshop"
PROXY_URL = 'http://localhost:3001'
PROXY_TIMEOUT = 20

socket_client.configure(
    app=APPLICATION, 
    url=PROXY_URL,
    timeout=PROXY_TIMEOUT
)

init(APPLICATION, socket_client)

@mcp.tool()
def set_active_document(document_id:int):
    """
    Sets the document with the specified ID to the active document in Photoshop

    Args:
        document_id (int): ID for the document to set as active.
    """

    command = createCommand("setActiveDocument", {
        "documentId":document_id
    })

    return sendCommand(command)

@mcp.tool()
def get_documents():
    """
    Returns information on the documents currently open in Photoshop
    """

    command = createCommand("getDocuments", {
    })

    return sendCommand(command)


@mcp.tool()
def create_gradient_layer_style(
    layer_id: int,
    angle: int,
    type:str,
    color_stops: list,
    opacity_stops: list):
    """
    Applies gradient to active selection or entire layer if no selection exists.

    Color stops define transition points along the gradient (0-100), with color blending between stops. Opacity stops similarly control transparency transitions.

    Args:
        layer_id (int): ID for layer to apply gradient to.
        angle (int): Gradient angle (-180 to 180).
        type (str): LINEAR or RADIAL gradient.
        color_stops (list): Dictionaries defining color stops:
            - location (int): Position (0-100) along gradient.
            - color (dict): RGB values (0-255 for red/green/blue).
            - midpoint (int): Transition bias (0-100, default 50).
        opacity_stops (list): Dictionaries defining opacity stops:
            - location (int): Position (0-100) along gradient.
            - opacity (int): Level (0=transparent, 100=opaque).
            - midpoint (int): Transition bias (0-100, default 50).
    """

    command = createCommand("createGradientLayerStyle", {
        "layerId":layer_id,
        "angle":angle,
        "colorStops":color_stops,
        "type":type,
        "opacityStops":opacity_stops
    })

    return sendCommand(command)


@mcp.tool()
def duplicate_document(document_name: str):
    """Duplicates the current Photoshop Document into a new file


        Args:
            document_name (str): Name for the new document being created
    """
    
    command = createCommand("duplicateDocument", {
        "name":document_name
    })

    return sendCommand(command)


@mcp.tool()
def create_document(document_name: str, width: int, height:int, resolution:int, fill_color:dict = {"red":0, "green":0, "blue":0}, color_mode:str = "RGB"):
    """Creates a new Photoshop Document

        Layer are created from bottom up based on the order they are created in, so create background elements first and then build on top.

        New document will contain a layer named "Background" that is filled with the specified fill color

        Args:
            document_name (str): Name for the new document being created
            width (int): Width in pixels of the new document
            height (int): Height in pixels of the new document
            resolution (int): Resolution (Pixels per Inch) of the new document
            fill_color (dict): dict defining the background color fill of the new document
            color_mode (str): Color mode for the new document
    """
    
    command = createCommand("createDocument", {
        "name":document_name,
        "width":width,
        "height":height,
        "resolution":resolution,
        "fillColor":fill_color,
        "colorMode":color_mode
    })

    return sendCommand(command)

@mcp.tool()
def export_layers_as_png(layers_info: list[dict[str, str|int]]):
    """Exports multiple layers from the Photoshop document as PNG files.
    
    This function exports each specified layer as a separate PNG image file to its 
    corresponding file path. The entire layer, including transparent space will be saved.
    
    Args:
        layers_info (list[dict[str, str|int]]): A list of dictionaries containing the export information.
            Each dictionary must have the following keys:
                - "layerId" (int): The ID of the layer to export as PNG. 
                   This layer must exist in the current document.
                - "filePath" (str): The absolute file path including filename where the PNG
                   will be saved (e.g., "/path/to/directory/layername.png").
                   The parent directory must already exist or the export will fail.
    """
    
    command = createCommand("exportLayersAsPng", {
        "layersInfo":layers_info
    })

    return sendCommand(command)



@mcp.tool()
def save_document_as(file_path: str, file_type: str = "PSD"):
    """Saves the current Photoshop document to the specified location and format.
    
    Args:
        file_path (str): The absolute path (including filename) where the file will be saved.
            Example: "/Users/username/Documents/my_image.psd"
        file_type (str, optional): The file format to use when saving the document.
            Defaults to "PSD".
            Supported formats:
                - "PSD": Adobe Photoshop Document (preserves layers and editability)
                - "PNG": Portable Network Graphics (lossless compression with transparency)
                - "JPG": Joint Photographic Experts Group (lossy compression)
    
    Returns:
        dict: Response from the Photoshop operation indicating success status, and the path that the file was saved at
    """
    
    command = createCommand("saveDocumentAs", {
        "filePath":file_path,
        "fileType":file_type
    })

    return sendCommand(command)

@mcp.tool()
def save_document():
    """Saves the current Photoshop Document
    """
    
    command = createCommand("saveDocument", {
    })

    return sendCommand(command)

@mcp.tool()
def group_layers(group_name: str, layer_ids: list[int]) -> list:
    """
    Creates a new layer group from the specified layers in Photoshop.

    Note: The layers will be added to the group in the order they are specified in the document, and not the order of their layerIds passed in. The group will be made at the same level as the top most layer in the layer tree.

    Args:
        groupName (str): The name to assign to the newly created layer group.
        layerIds (list[int]): A list of layer ids to include in the new group.

    Raises:
        RuntimeError: If the operation fails or times out.

    """


    command = createCommand("groupLayers", {
        "groupName":group_name,
        "layerIds":layer_ids
    })

    return sendCommand(command)


@mcp.tool()
def get_layer_image(layer_id: int):
    """Returns a jpeg of the specified layer's content as an MCP Image object that can be displayed."""

    command = createCommand("getLayerImage",
        {
            "layerId":layer_id
        }
    )

    response = sendCommand(command)

    if response.get('status') == 'SUCCESS' and 'response' in response:
        image_data = response['response']
        data_url = image_data.get('dataUrl')

        if data_url and data_url.startswith("data:image/jpeg;base64,"):
            # Strip the data URL prefix and decode the base64 JPEG bytes
            base64_data = data_url.split(",", 1)[1]
            jpeg_bytes = base64.b64decode(base64_data)

            return Image(data=jpeg_bytes, format="jpeg")

    return response


@mcp.tool()
def get_document_image():
    """Returns a jpeg of the current visible Photoshop document as an MCP Image object that can be displayed."""
    command = createCommand("getDocumentImage", {})
    response = sendCommand(command)

    if response.get('status') == 'SUCCESS' and 'response' in response:
        image_data = response['response']
        data_url = image_data.get('dataUrl')

        if data_url and data_url.startswith("data:image/jpeg;base64,"):
            # Strip the data URL prefix and decode the base64 JPEG bytes
            base64_data = data_url.split(",", 1)[1]
            jpeg_bytes = base64.b64decode(base64_data)

            return Image(data=jpeg_bytes, format="jpeg")

    return response

@mcp.tool()
def save_document_image_as_png(file_path: str):
    """
    Capture the Photoshop document and save as PNG file
    
    Args:
        file_path: Where to save the PNG file
        
    Returns:
        dict: Status and file info
    """
    command = createCommand("getDocumentImage", {})
    response = sendCommand(command)
    
    if response.get('format') == 'raw' and 'rawDataBase64' in response:
        try:
            # Decode raw data
            raw_bytes = base64.b64decode(response['rawDataBase64'])
            
            # Extract metadata
            width = response['width']
            height = response['height']
            components = response['components']
            
            # Convert to numpy array and reshape
            pixel_array = np.frombuffer(raw_bytes, dtype=np.uint8)
            image_array = pixel_array.reshape((height, width, components))
            
            # Create and save PNG
            mode = 'RGBA' if components == 4 else 'RGB'
            image = Image.fromarray(image_array, mode)
            image.save(file_path, 'PNG')
            
            return {
                'status': 'success',
                'file_path': file_path,
                'width': width,
                'height': height,
                'size_bytes': os.path.getsize(file_path)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    else:
        return {
            'status': 'error',
            'error': 'No raw image data received'
        }

@mcp.tool()
def get_layers() -> list:
    """Returns a nested list of dicts that contain layer info and the order they are arranged in.

    Args:
        None
        
    Returns:
        list: A nested list of dictionaries containing layer information and hierarchy.
            Each dict has at minimum a 'name' key with the layer name.
            If a layer has sublayers, they will be contained in a 'layers' key which contains another list of layer dicts.
            Example: [{'name': 'Group 1', 'layers': [{'name': 'Layer 1'}, {'name': 'Layer 2'}]}, {'name': 'Background'}]
    """

    command = createCommand("getLayers", {})

    return sendCommand(command)


@mcp.tool()
def place_image(
    layer_id: int,
    image_path: str
):
    """Places the image at the specified path on the existing pixel layer with the specified id.

    The image will be placed on the center of the layer, and will fill the layer without changing its aspect ration (thus there may be bars at the top or bottom) 

    Args:
        layer_id (int): The id of the layer where the image will be placed.
        image_path (str): The file path to the image that will be placed on the layer.
    """
    
    command = createCommand("placeImage", {
        "layerId":layer_id,
        "imagePath":image_path
    })

    return sendCommand(command)

@mcp.tool()
def harmonize_layer(layer_id:int,  new_layer_name:str, rasterize_layer:bool = True):
    """Harmonizes (matches lighting and other settings) the selected layer with the background layers.

    The layer being harmonized should be rasterized and have some transparency.

    Args:
        layer_id (int): ID of the layer to be harmonizes.
        new_layer_name (str): Name for the new layer that will be created with the harmonized content
        rasterize_layer (bool): Whether the new layer should be rasterized.
            If not rasterized, the layer will remain a generative layer which
            allows the user to interact with it. True by default.
    """

    command = createCommand("harmonizeLayer", {
        "layerId":layer_id,
         "newLayerName":new_layer_name,
        "rasterizeLayer":rasterize_layer
    })

    return sendCommand(command)


@mcp.tool()
def rename_layers(
    layer_data: list[dict]
):
    """Renames one or more layers

    Args:
        layer_data (list[dict]): A list of dictionaries containing layer rename information.
            Each dictionary must have the following keys:
                - "layer_id" (int): ID of the layer to be renamed.
                - "new_layer_name" (str): New name for the layer.
    """
    
    command = createCommand("renameLayers", {
        "layerData":layer_data
    })
    
    return sendCommand(command)


@mcp.tool()
def scale_layer(
    layer_id:int,
    width:int,
    height:int,
    anchor_position:str,
    interpolation_method:str = "AUTOMATIC"
):
    """Scales the layer with the specified ID.

    Args:
        layer_id (int): ID of layer to be scaled.
        width (int): Percentage to scale horizontally.
        height (int): Percentage to scale vertically.
        anchor_position (str): The anchor position to rotate around,
        interpolation_method (str): Interpolation method to use when resampling the image
    """
    
    command = createCommand("scaleLayer", {
        "layerId":layer_id,
        "width":width,
        "height":height,
        "anchorPosition":anchor_position,
        "interpolationMethod":interpolation_method
    })

    return sendCommand(command)


@mcp.tool()
def rotate_layer(
    layer_id:int,
    angle:int,
    anchor_position:str,
    interpolation_method:str = "AUTOMATIC"
):
    """Rotates the layer with the specified ID.

    Args:
        layer_id (int): ID of layer to be scaled.
        angle (int): Angle (-359 to 359) to rotate the layer by in degrees
        anchor_position (str): The anchor position to rotate around,
        interpolation_method (str): Interpolation method to use when resampling the image
    """
    
    command = createCommand("rotateLayer", {
        "layerId":layer_id,
        "angle":angle,
        "anchorPosition":anchor_position,
        "interpolationMethod":interpolation_method
    })

    return sendCommand(command)


@mcp.tool()
def flip_layer(
    layer_id:int,
    axis:str
):
    """Flips the layer with the specified ID on the specified axis.

    Args:
        layer_id (int): ID of layer to be scaled.
        axis (str): The axis on which to flip the layer. Valid values are "horizontal", "vertical" or "both"
    """
    
    command = createCommand("flipLayer", {
        "layerId":layer_id,
        "axis":axis
    })

    return sendCommand(command)


@mcp.tool()
def delete_layer(
    layer_id:int
):
    """Deletes the layer with the specified ID

    Args:
        layer_id (int): ID of the layer to be deleted
    """
    
    command = createCommand("deleteLayer", {
        "layerId":layer_id
    })

    return sendCommand(command)



@mcp.tool()
def set_layer_visibility(
    layer_id:int,
    visible:bool
):
    """Sets the visibility of the layer with the specified ID

    Args:
        layer_id (int): ID of the layer to set visibility
        visible (bool): Whether the layer is visible
    """
    
    command = createCommand("setLayerVisibility", {
        "layerId":layer_id,
        "visible":visible
    })

    return sendCommand(command)


@mcp.tool()
def generate_image(
    layer_name:str,
    prompt:str,
    content_type:str = "none"
):
    """Uses Adobe Firefly Generative AI to generate an image on a new layer with the specified layer name.

    If there is an active selection, it will use that region for the generation. Otherwise it will generate
    on the entire layer.

    Args:
        layer_name (str): Name for the layer that will be created and contain the generated image
        prompt (str): Prompt describing the image to be generated
        content_type (str): The type of image to be generated. Options include "photo", "art" or "none" (default)
    """
    
    command = createCommand("generateImage", {
        "layerName":layer_name,
        "prompt":prompt,
        "contentType":content_type
    })

    return sendCommand(command)

@mcp.tool()
def generative_fill(
    layer_name: str,
    prompt: str,
    layer_id: int,
    content_type: str = "none"
):
    """Uses Adobe Firefly Generative AI to perform generative fill within the current selection.

    This function uses generative fill to seamlessly integrate new content into the existing image.
    It requires an active selection, and will fill that region taking into account the surrounding 
    context and layers below. The AI considers the existing content to create a natural, 
    contextually-aware fill.

    Args:
        layer_name (str): Name for the layer that will be created and contain the generated fill
        prompt (str): Prompt describing the content to be generated within the selection
        layer_id (int): ID of the layer to work with (though a new layer is created for the result)
        content_type (str): The type of image to be generated. Options include "photo", "art" or "none" (default)
    
    Returns:
        dict: Response from Photoshop containing the operation status and layer information
    """

    command = createCommand("generativeFill", {
        "layerName":layer_name,
        "prompt":prompt,
        "layerId":layer_id,
        "contentType":content_type,
    })

    return sendCommand(command)


@mcp.tool()
def move_layer(
    layer_id:int,
    position:str
):
    """Moves the layer within the layer stack based on the specified position

    Args:
        layer_id (int): Name for the layer that will be moved
        position (str): How the layer position within the layer stack will be updated. Value values are: TOP (Place above all layers), BOTTOM (Place below all layers), UP (Move up one layer), DOWN (Move down one layer)
    """

    command = createCommand("moveLayer", {
        "layerId":layer_id,
        "position":position
    })

    return sendCommand(command)

@mcp.tool()
def get_document_info():
    """Retrieves information about the currently active document.

    Returns:
        response : An object containing the following document properties:
            - height (int): The height of the document in pixels.
            - width (int): The width of the document in pixels.
            - colorMode (str): The document's color mode as a string.
            - pixelAspectRatio (float): The pixel aspect ratio of the document.
            - resolution (float): The document's resolution (DPI).
            - path (str): The file path of the document, if saved.
            - saved (bool): Whether the document has been saved (True if it has a valid file path).
            - hasUnsavedChanges (bool): Whether the document contains unsaved changes.

    """

    command = createCommand("getDocumentInfo", {})

    return sendCommand(command)

@mcp.tool()
def crop_document():
    """Crops the document to the active selection.

    This function removes all content outside the selection area and resizes the document 
    so that the selection becomes the new canvas size.

    An active selection is required.
    """

    command = createCommand("cropDocument", {})

    return sendCommand(command)

@mcp.tool()
def paste_from_clipboard(layer_id: int, paste_in_place: bool = True):
    """Pastes the current clipboard contents onto the specified layer.

    If `paste_in_place` is True, the content will be positioned exactly where it was cut or copied from.
    If False and an active selection exists, the content will be centered within the selection.
    If no selection is active, the content will be placed at the center of the layer.

    Args:
        layer_id (int): The ID of the layer where the clipboard contents will be pasted.
        paste_in_place (bool): Whether to paste at the original location (True) or adjust based on selection/layer center (False).
    """


    command = createCommand("pasteFromClipboard", {
        "layerId":layer_id,
        "pasteInPlace":paste_in_place
    })

    return sendCommand(command)

@mcp.tool()
def rasterize_layer(layer_id: int):
    """Converts the specified layer into a rasterized (flat) image.

    This process removes any vector, text, or smart object properties, turning the layer 
    into pixel-based content.

    Args:
        layer_id (int): The name of the layer to rasterize.
    """

    command = createCommand("rasterizeLayer", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def open_photoshop_file(file_path: str):
    """Opens the specified Photoshop-compatible file within Photoshop.

    This function attempts to open a file in Adobe Photoshop. The file must be in a 
    format compatible with Photoshop, such as PSD, TIFF, JPEG, PNG, etc.

    Args:
        file_path (str): Complete absolute path to the file to be opened, including filename and extension.

    Returns:
        dict: Response from the Photoshop operation indicating success status.
        
    Raises:
        RuntimeError: If the file doesn't exist, is not accessible, or is in an unsupported format.
    """

    command = createCommand("openFile", {
        "filePath":file_path
    })

    return sendCommand(command)

@mcp.tool()
def cut_selection_to_clipboard(layer_id: int):
    """Copies and removes (cuts) the selected pixels from the specified layer to the system clipboard.

    This function requires an active selection.

    Args:
        layer_id (int): The name of the layer that contains the pixels to copy and remove.
    """

    command = createCommand("cutSelectionToClipboard", {
        "layerId":layer_id
    })

    return sendCommand(command)


@mcp.tool()
def copy_merged_selection_to_clipboard():
    """Copies the selected pixels from all visible layers to the system clipboard.

    This function requires an active selection. If no selection is active, the operation will fail.
    The copied content will include pixel data from all visible layers within the selection area,
    effectively capturing what you see on screen.

    Returns:
        dict: Response from the Photoshop operation indicating success status.
        
    Raises:
        RuntimeError: If no active selection exists.
    """

    command = createCommand("copyMergedSelectionToClipboard", {})

    return sendCommand(command)

@mcp.tool()
def copy_selection_to_clipboard(layer_id: int):
    """Copies the selected pixels from the specified layer to the system clipboard.

    This function requires an active selection. If no selection is active, the operation will fail.

    Args:
        layer_id (int): The name of the layer that contains the pixels to copy.
        
    Returns:
        dict: Response from the Photoshop operation indicating success status.
    """

    command = createCommand("copySelectionToClipboard", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def select_subject(layer_id: int):
    """Automatically selects the subject in the specified layer.

    This function identifies and selects the subject in the given image layer. 
    It returns an object containing a property named `hasActiveSelection`, 
    which indicates whether any pixels were selected (e.g., if no subject was detected).

    Args:
        layer_int (int): The name of that contains the image to select the subject from.
    """

    
    command = createCommand("selectSubject", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def select_sky(layer_id: int):
    """Automatically selects the sky in the specified layer.

    This function identifies and selects the sky in the given image layer. 
    It returns an object containing a property named `hasActiveSelection`, 
    which indicates whether any pixels were selected (e.g., if no sky was detected).

    Args:
        layer_id (int): The name of that contains the image to select the sky from.
    """

    
    command = createCommand("selectSky", {
        "layerId":layer_id
    })

    return sendCommand(command)


@mcp.tool()
def get_layer_bounds(
    layer_id: int
):
    """Returns the pixel bounds for the layer with the specified ID
    
    Args:
        layer_id (int): ID of the layer to get the bounds information from

    Returns:
        dict: A dictionary containing the layer bounds with the following properties:
            - left (int): The x-coordinate of the left edge of the layer
            - top (int): The y-coordinate of the top edge of the layer
            - right (int): The x-coordinate of the right edge of the layer
            - bottom (int): The y-coordinate of the bottom edge of the layer
            
    Raises:
        RuntimeError: If the layer doesn't exist or if the operation fails
    """
    
    command = createCommand("getLayerBounds", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def remove_background(
    layer_id:int
):
    """Automatically removes the background of the image in the layer with the specified ID and keeps the main subject
    
    Args:
        layer_id (int): ID of the layer to remove the background from
    """
    
    command = createCommand("removeBackground", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def create_pixel_layer(
    layer_name:str,
    fill_neutral:bool,
    opacity:int = 100,
    blend_mode:str = "NORMAL",
):
    """Creates a new pixel layer with the specified ID
    
    Args:
        layer_name (str): Name of the new layer being created
        fill_neutral (bool): Whether to fill the layer with a neutral color when applying Blend Mode.
        opacity (int): Opacity of the newly created layer
        blend_mode (str): Blend mode of the newly created layer
    """
    
    command = createCommand("createPixelLayer", {
        "layerName":layer_name,
        "opacity":opacity,
        "fillNeutral":fill_neutral,
        "blendMode":blend_mode
    })

    return sendCommand(command)

@mcp.tool()
def create_multi_line_text_layer(
    layer_name:str, 
    text:str, 
    font_size:int, 
    postscript_font_name:str, 
    opacity:int = 100,
    blend_mode:str = "NORMAL",
    text_color:dict = {"red":255, "green":255, "blue":255}, 
    position:dict = {"x": 100, "y":100},
    bounds:dict = {"top": 0, "left": 0, "bottom": 250, "right": 300},
    justification:str = "LEFT"
    ):

    """
    Creates a new multi-line text layer with the specified ID within the current Photoshop document.
    
    Args:
        layer_name (str): The name of the layer to be created. Can be used to select in other api calls.
        text (str): The text to include on the layer.
        font_size (int): Font size.
        postscript_font_name (string): Postscript Font Name to display the text in. Valid list available via get_option_info.
        opacity (int): Opacity for the layer specified in percent.
        blend_mode (str): Blend Mode for the layer. Valid list available via get_option_info
        text_color (dict): Color of the text expressed in Red, Green, Blue values between 0 and 255
        position (dict): Position (dict with x, y values) where the text will be placed in the layer. Based on bottom left point of the text.
        bounds (dict): text bounding box
        justification (str): text justification. Valid list available via get_option_info.
    """

    command = createCommand("createMultiLineTextLayer", {
        "layerName":layer_name,
        "contents":text,
        "fontSize": font_size,
        "opacity":opacity,
        "position":position,
        "fontName":postscript_font_name,
        "textColor":text_color,
        "blendMode":blend_mode,
        "bounds":bounds,
        "justification":justification
    })

    return sendCommand(command)


@mcp.tool()
def create_single_line_text_layer(
    layer_name:str, 
    text:str, 
    font_size:int, 
    postscript_font_name:str, 
    opacity:int = 100,
    blend_mode:str = "NORMAL",
    text_color:dict = {"red":255, "green":255, "blue":255}, 
    position:dict = {"x": 100, "y":100}
    ):

    """
    Create a new single line text layer with the specified ID within the current Photoshop document.
    
     Args:
        layer_name (str): The name of the layer to be created. Can be used to select in other api calls.
        text (str): The text to include on the layer.
        font_size (int): Font size.
        postscript_font_name (string): Postscript Font Name to display the text in. Valid list available via get_option_info.
        opacity (int): Opacity for the layer specified in percent.
        blend_mode (str): Blend Mode for the layer. Valid list available via get_option_info
        text_color (dict): Color of the text expressed in Red, Green, Blue values between 0 and 255
        position (dict): Position (dict with x, y values) where the text will be placed in the layer. Based on bottom left point of the text.
    """

    command = createCommand("createSingleLineTextLayer", {
        "layerName":layer_name,
        "contents":text,
        "fontSize": font_size,
        "opacity":opacity,
        "position":position,
        "fontName":postscript_font_name,
        "textColor":text_color,
        "blendMode":blend_mode
    })

    return sendCommand(command)

@mcp.tool()
def edit_text_layer(
    layer_id:int, 
    text:str = None,
    font_size:int = None,
    postscript_font_name:str = None, 
    text_color:dict = None,
    ):

    """
    Edits the text content of an existing text layer in the current Photoshop document.
    
    Args:
        layer_id (int): The ID of the existing text layer to edit.
        text (str): The new text content to replace the current text in the layer. If None, text will not be changed.
        font_size (int): Font size. If None, size will not be changed.
        postscript_font_name (string): Postscript Font Name to display the text in. Valid list available via get_option_info. If None, font will not will not be changed.
        text_color (dict): Color of the text expressed in Red, Green, Blue values between 0 and 255 in format of {"red":255, "green":255, "blue":255}. If None, color will not be changed
    """

    command = createCommand("editTextLayer", {
        "layerId":layer_id,
        "contents":text,
        "fontSize": font_size,
        "fontName":postscript_font_name,
        "textColor":text_color
    })

    return sendCommand(command)



@mcp.tool()
def translate_layer(
    layer_id: int,
    x_offset:int = 0,
    y_offset:int = 0
    ):

    """
        Moves the layer with the specified ID on the X and Y axis by the specified number of pixels.

    Args:
        layer_name (str): The name of the layer that should be moved.
        x_offset (int): Amount to move on the horizontal axis. Negative values move the layer left, positive values right
        y_offset (int): Amount to move on the vertical axis. Negative values move the layer down, positive values up
    """
    
    command = createCommand("translateLayer", {
        "layerId":layer_id,
        "xOffset":x_offset,
        "yOffset":y_offset
    })

    return sendCommand(command)

@mcp.tool()
def set_layer_position_absolute(
    layer_id: int,
    x: int,
    y: int
    ):
    """Moves a layer to an absolute x,y position (top-left corner of layer bounds).

    Unlike translate_layer which moves by offset, this sets the exact position.

    Args:
        layer_id (int): ID of the layer to move
        x (int): Target X coordinate for the layer's left edge
        y (int): Target Y coordinate for the layer's top edge
    """
    command = createCommand("setLayerPositionAbsolute", {
        "layerId": layer_id,
        "x": x,
        "y": y
    })
    return sendCommand(command)

@mcp.tool()
def remove_layer_mask(
    layer_id: int
    ):

    """Removes the layer mask from the specified layer.

    Args:
        None
    """
    
    command = createCommand("removeLayerMask", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def add_layer_mask_from_selection(
    layer_id: int
    ):

    """Creates a layer mask on the specified layer defined by the active selection.
    
    This function takes the current active selection in the document and converts it into a layer mask
    for the specified layer. Selected areas will be visible, while non-selected areas will be hidden.
    An active selection must exist before calling this function.

    Args:
        layer_name (str): The name of the layer to which the mask will be applied
    """
    
    command = createCommand("addLayerMask", {
        "layerId":layer_id
    })

    return sendCommand(command)

@mcp.tool()
def set_layer_properties(
    layer_id: int,
    blend_mode: str = "NORMAL",
    layer_opacity: int = 100,
    fill_opacity: int = 100,
    is_clipping_mask: bool = False
    ):

    """Sets the blend mode and opacity properties on the layer with the specified ID

    Args:
        layer_id (int): The ID of the layer whose properties should be updated
        blend_mode (str): The blend mode for the layer
        layer_opacity (int): The opacity for the layer (0 - 100)
        fill_opacity (int): The fill opacity for the layer (0 - 100). Will ignore anny effects that have been applied to the layer.
        is_clipping_mask (bool): A boolean indicating whether this layer will be clipped to (masked by) the layer below it
    """
    
    command = createCommand("setLayerProperties", {
        "layerId":layer_id,
        "blendMode":blend_mode,
        "layerOpacity":layer_opacity,
        "fillOpacity":fill_opacity,
        "isClippingMask":is_clipping_mask
    })

    return sendCommand(command)

@mcp.tool()
def fill_selection(
    layer_id: int,
    color:dict = {"red":255, "green":0, "blue":0},
    blend_mode:str = "NORMAL",
    opacity:int = 100,
    ):

    """Fills the selection on the pixel layer with the specified ID
    
    Args:
        layer_id (int): The ID of existing pixel layer to add the fill
        color (dict): The color of the fill
        blend_mode (dict): The blend mode for the fill
        opacity (int) : The opacity of the color for the fill
    """
    
    command = createCommand("fillSelection", {
        "layerId":layer_id,
        "color":color,
        "blendMode":blend_mode,
        "opacity":opacity
    })

    return sendCommand(command)



@mcp.tool()
def delete_selection(
    layer_id: int
    ):

    """Removes the pixels within the selection on the pixel layer with the specified ID
    
    Args:
        layer_id (int): The ID of the layer from which the content of the selection should be deleted
    """
    
    command = createCommand("deleteSelection", {
        "layerId":layer_id
    })

    return sendCommand(command)


@mcp.tool()
def invert_selection():
    
    """Inverts the current selection in the Photoshop document"""

    command = createCommand("invertSelection", {})
    return sendCommand(command)


@mcp.tool()
def clear_selection():
    
    """Clears / deselects the current selection"""

    command = createCommand("clearSelection", {})

    return sendCommand(command)

@mcp.tool()
def select_rectangle(
    layer_id:int,
    feather:int = 0,
    anti_alias:bool = True,
    bounds:dict = {"top": 0, "left": 0, "bottom": 100, "right": 100}
    ):
    
    """Creates a rectangular selection and selects the specified layer
    
    Args:
        layer_id (int): The layer to do the select rectangle action on.
        feather (int): The amount of feathering in pixels to apply to the selection (0 - 1000)
        anti_alias (bool): Whether anti-aliases is applied to the selection
        bounds (dict): The bounds for the rectangle selection
    """

    command = createCommand("selectRectangle", {
        "layerId":layer_id,
        "feather":feather,
        "antiAlias":anti_alias,
        "bounds":bounds
    })

    return sendCommand(command)

@mcp.tool()
def select_polygon(
    layer_id:int,
    feather:int = 0,
    anti_alias:bool = True,
    points:list[dict[str, int]] = [{"x": 50, "y": 10}, {"x": 100, "y": 90}, {"x": 10, "y": 40}]
    ):
    
    """Creates an n-sided polygon selection and selects the specified layer
    
    Args:
        layer_id (int): The layer to do the selection action on.
        feather (int): The amount of feathering in pixels to apply to the selection (0 - 1000)
        anti_alias (bool): Whether anti-aliases is applied to the selection
        points (list): The points that define the sides of the selection, defined via a list of dicts with x, y values.
    """

    command = createCommand("selectPolygon", {
        "layerId":layer_id,
        "feather":feather,
        "antiAlias":anti_alias,
        "points":points
    })

    return sendCommand(command)

@mcp.tool()
def select_ellipse(
    layer_id:int,
    feather:int = 0,
    anti_alias:bool = True,
    bounds:dict = {"top": 0, "left": 0, "bottom": 100, "right": 100}
    ):
    
    """Creates an elliptical selection and selects the specified layer
    
    Args:
        layer_id (int): The layer to do the selection action on.
        feather (int): The amount of feathering in pixels to apply to the selection (0 - 1000)
        anti_alias (bool): Whether anti-aliases is applied to the selection
        bounds (dict): The bounds that will define the elliptical selection.
    """

    command = createCommand("selectEllipse", {
        "layerId":layer_id,
        "feather":feather,
        "antiAlias":anti_alias,
        "bounds":bounds
    })

    return sendCommand(command)

@mcp.tool()
def align_content(
    layer_id: int,
    alignment_mode:str
    ):
    
    """
    Aligns content on layer with the specified ID to the current selection.

    Args:
        layer_id (int): The ID of the layer in which to align the content
        alignment_mode (str): How the content should be aligned. Available options via alignment_modes
    """

    command = createCommand("alignContent", {
        "layerId":layer_id,
        "alignmentMode":alignment_mode
    })

    return sendCommand(command)

@mcp.tool()
def add_drop_shadow_layer_style(
    layer_id: int,
    blend_mode:str = "MULTIPLY",
    color:dict = {"red":0, "green":0, "blue":0},
    opacity:int = 35,
    angle:int = 160,
    distance:int = 3,
    spread:int = 0,
    size:int = 7
    ):
    """Adds a drop shadow layer style to the layer with the specified ID

    Args:
        layer_id (int): The ID for the layer with the content to add the drop shadow to
        blend_mode (str): The blend mode for the drop shadow
        color (dict): The color for the drop shadow
        opacity (int): The opacity of the drop shadow
        angle (int): The angle (-180 to 180) of the drop shadow relative to the content
        distance (int): The distance in pixels of the drop shadow (0 to 30000)
        spread (int): Defines how gradually the shadow fades out at its edges, with higher values creating a harsher, more defined edge, and lower values a softer, more feathered edge (0 to 100)
        size (int): Control the blur and spread of the shadow effect (0 to 250)
    """

    command = createCommand("addDropShadowLayerStyle", {
        "layerId":layer_id,
        "blendMode":blend_mode,
        "color":color,
        "opacity":opacity,
        "angle":angle,
        "distance":distance,
        "spread":spread,
        "size":size
    })

    return sendCommand(command)

@mcp.tool()
def duplicate_layer(layer_to_duplicate_id:int, duplicate_layer_name:str):
    """
    Duplicates the layer specified by layer_to_duplicate_id ID, creating a new layer above it with the name specified by duplicate_layer_name

    Args:
        layer_to_duplicate_id (id): The id of the layer to be duplicated
        duplicate_layer_name (str): Name for the newly created layer
    """

    command = createCommand("duplicateLayer", {
        "sourceLayerId":layer_to_duplicate_id,
        "duplicateLayerName":duplicate_layer_name,
    })

    return sendCommand(command)

@mcp.tool()
def flatten_all_layers(layer_name:str):
    """
    Flatten all layers in the document into a single layer with specified name

    Args:
        layer_name (str): The name of the merged layer
    """

    command = createCommand("flattenAllLayers", {
        "layerName":layer_name,
    })

    return sendCommand(command)

@mcp.tool()
def add_color_balance_adjustment_layer(
    layer_id: int,
    highlights:list = [0,0,0],
    midtones:list = [0,0,0],
    shadows:list = [0,0,0]):
    """Adds an adjustment layer to the layer with the specified ID to adjust color balance

    Each property highlights, midtones and shadows contains an array of 3 values between
    -100 and 100 that represent the relative position between two colors.

    First value is between cyan and red
    The second value is between magenta and green
    The third value is between yellow and blue    

    Args:
        layer_id (int): The ID of the layer to apply the color balance adjustment layer
        highlights (list): Relative color values for highlights
        midtones (list): Relative color values for midtones
        shadows (list): Relative color values for shadows
    """

    command = createCommand("addColorBalanceAdjustmentLayer", {
        "layerId":layer_id,
        "highlights":highlights,
        "midtones":midtones,
        "shadows":shadows
    })

    return sendCommand(command)

@mcp.tool()
def add_brightness_contrast_adjustment_layer(
    layer_id: int,
    brightness:int = 0,
    contrast:int = 0):
    """Adds an adjustment layer to the layer with the specified ID to adjust brightness and contrast

    Args:
        layer_id (int): The ID of the layer to apply the brightness and contrast adjustment layer
        brightness (int): The brightness value (-150 to 150)
        contrasts (int): The contrast value (-50 to 100)
    """

    command = createCommand("addBrightnessContrastAdjustmentLayer", {
        "layerId":layer_id,
        "brightness":brightness,
        "contrast":contrast
    })

    return sendCommand(command)


@mcp.tool()
def add_stroke_layer_style(
    layer_id: int,
    size: int = 2,
    color: dict = {"red": 0, "green": 0, "blue": 0},
    opacity: int = 100,
    position: str = "CENTER",
    blend_mode: str = "NORMAL"
    ):
    """Adds a stroke layer style to the layer with the specified ID.
    
    Args:
        layer_id (int): The ID of the layer to apply the stroke effect to.
        size (int, optional): The width of the stroke in pixels. Defaults to 2.
        color (dict, optional): The color of the stroke as RGB values. Defaults to black {"red": 0, "green": 0, "blue": 0}.
        opacity (int, optional): The opacity of the stroke as a percentage (0-100). Defaults to 100.
        position (str, optional): The position of the stroke relative to the layer content. 
                                 Options include "CENTER", "INSIDE", or "OUTSIDE". Defaults to "CENTER".
        blend_mode (str, optional): The blend mode for the stroke effect. Defaults to "NORMAL".
    """

    command = createCommand("addStrokeLayerStyle", {
        "layerId":layer_id,
        "size":size,
        "color":color,
        "opacity":opacity,
        "position":position,
        "blendMode":blend_mode
    })

    return sendCommand(command)


@mcp.tool()
def add_vibrance_adjustment_layer(
    layer_id: int,
    vibrance:int = 0,
    saturation:int = 0):
    """Adds an adjustment layer to layer with the specified ID to adjust vibrance and saturation
    
    Args:
        layer_id (int): The ID of the layer to apply the vibrance and saturation adjustment layer
        vibrance (int): Controls the intensity of less-saturated colors while preventing oversaturation of already-saturated colors. Range -100 to 100.
        saturation (int): Controls the intensity of all colors equally. Range -100 to 100.
    """
    #0.1 to 255

    command = createCommand("addAdjustmentLayerVibrance", {
        "layerId":layer_id,
        "saturation":saturation,
        "vibrance":vibrance
    })

    return sendCommand(command)

@mcp.tool()
def add_black_and_white_adjustment_layer(
    layer_id: int,
    colors: dict = {"blue": 20, "cyan": 60, "green": 40, "magenta": 80, "red": 40, "yellow": 60},
    tint: bool = False,
    tint_color: dict = {"red": 225, "green": 211, "blue": 179}
):
    """Adds a Black & White adjustment layer to the specified layer.
    
    Creates an adjustment layer that converts the target layer to black and white. Optionally applies a color tint to the result.
    
    Args:
        layer_id (int): The ID of the layer to apply the black and white adjustment to.
        colors (dict): Controls how each color channel converts to grayscale. Values range from 
                      -200 to 300, with higher values making that color appear lighter in the 
                      conversion. Must include all keys: red, yellow, green, cyan, blue, magenta.
        tint (bool, optional): Whether to apply a color tint to the black and white result.
                              Defaults to False.
        tint_color (dict, optional): The RGB color dict to use for tinting
                                    with "red", "green", and "blue" keys (values 0-255).
    """

    command = createCommand("addAdjustmentLayerBlackAndWhite", {
        "layerId":layer_id,
        "colors":colors,
        "tint":tint,
        "tintColor":tint_color
    })

    return sendCommand(command)

@mcp.tool()
def apply_gaussian_blur(layer_id: int, radius: float = 2.5):
    """Applies a Gaussian Blur to the layer with the specified ID
    
    Args:
        layer_id (int): ID of layer to be blurred
        radius (float): The blur radius in pixels determining the intensity of the blur effect. Default is 2.5.
        Valid values range from 0.1 (subtle blur) to 10000 (extreme blur).

    Returns:
        dict: Response from the Photoshop operation
        
    Raises:
        RuntimeError: If the operation fails or times out
    """



    command = createCommand("applyGaussianBlur", {
        "layerId":layer_id,
        "radius":radius,
    })

    return sendCommand(command)




@mcp.tool()
def apply_motion_blur(layer_id: int, angle: int = 0, distance: float = 30):
    """Applies a Motion Blur to the layer with the specified ID

    Args:
    layer_id (int): ID of layer to be blurred
    angle (int): The angle in degrees (0 to 360) that determines the direction of the motion blur effect. Default is 0.
    distance (float): The distance in pixels that controls the length/strength of the motion blur. Default is 30.
        Higher values create a more pronounced motion effect.

    Returns:
        dict: Response from the Photoshop operation
        
    Raises:
        RuntimeError: If the operation fails or times out
    """


    command = createCommand("applyMotionBlur", {
        "layerId":layer_id,
        "angle":angle,
        "distance":distance
    })

    return sendCommand(command)


@mcp.tool()
def apply_noise(layer_id: int, amount: float = 5.0, distribution: str = "gaussian", monochromatic: bool = True):
    """Applies a Noise filter to the layer with the specified ID

    Args:
        layer_id (int): ID of layer to add noise to
        amount (float): The amount of noise to add (0.1 to 400). Default is 5.0.
        distribution (str): The distribution type - "uniform" or "gaussian". Default is "gaussian".
        monochromatic (bool): Whether to use monochromatic noise. Default is True.

    Returns:
        dict: Response from the Photoshop operation
        
    Raises:
        RuntimeError: If the operation fails or times out
    """

    command = createCommand("applyNoise", {
        "layerId": layer_id,
        "amount": amount,
        "distribution": distribution,
        "monochromatic": monochromatic
    })

    return sendCommand(command)


# =============================================================================
# FILTERS - New expanded filters (20 new)
# =============================================================================

@mcp.tool()
def apply_sharpen(layer_id: int):
    """Applies a basic Sharpen filter to the layer with the specified ID.

    Args:
        layer_id (int): ID of the layer to sharpen
    """
    command = createCommand("applySharpen", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def apply_unsharp_mask(layer_id: int, amount: int = 100, radius: float = 1.0, threshold: int = 0):
    """Applies Unsharp Mask filter to sharpen the layer.

    Args:
        layer_id (int): ID of the layer to sharpen
        amount (int): Sharpening strength in percent (1-500). Default 100.
        radius (float): Pixel radius of sharpening effect (0.1-1000). Default 1.0.
        threshold (int): Difference threshold before sharpening is applied (0-255). Default 0.
    """
    command = createCommand("applyUnsharpMask", {
        "layerId": layer_id,
        "amount": amount,
        "radius": radius,
        "threshold": threshold
    })
    return sendCommand(command)

@mcp.tool()
def apply_high_pass(layer_id: int, radius: float = 10.0):
    """Applies High Pass filter. Useful for advanced sharpening when combined with Overlay blend mode.

    Args:
        layer_id (int): ID of the layer
        radius (float): Radius in pixels (0.1-1000). Default 10.0.
    """
    command = createCommand("applyHighPass", {"layerId": layer_id, "radius": radius})
    return sendCommand(command)

@mcp.tool()
def apply_radial_blur(layer_id: int, amount: int = 10, method: str = "spin", quality: str = "good"):
    """Applies Radial Blur filter for spin or zoom effects.

    Args:
        layer_id (int): ID of the layer
        amount (int): Blur intensity (1-100). Default 10.
        method (str): 'spin' or 'zoom'. Default 'spin'.
        quality (str): 'draft', 'good', or 'best'. Default 'good'.
    """
    command = createCommand("applyRadialBlur", {
        "layerId": layer_id,
        "amount": amount,
        "method": method,
        "quality": quality
    })
    return sendCommand(command)

@mcp.tool()
def apply_surface_blur(layer_id: int, radius: int = 5, threshold: int = 15):
    """Applies Surface Blur filter. Blurs surfaces while preserving edges.

    Args:
        layer_id (int): ID of the layer
        radius (int): Blur radius (1-100). Default 5.
        threshold (int): Tonal threshold for edge detection (2-255). Default 15.
    """
    command = createCommand("applySurfaceBlur", {
        "layerId": layer_id,
        "radius": radius,
        "threshold": threshold
    })
    return sendCommand(command)

@mcp.tool()
def apply_lens_blur(layer_id: int, radius: int = 15, brightness: int = 0, threshold: int = 255):
    """Applies Lens Blur filter for depth-of-field bokeh effects.

    Args:
        layer_id (int): ID of the layer
        radius (int): Blur radius (0-100). Default 15.
        brightness (int): Specular highlight brightness (0-100). Default 0.
        threshold (int): Brightness threshold for specular highlights (0-255). Default 255.
    """
    command = createCommand("applyLensBlur", {
        "layerId": layer_id,
        "radius": radius,
        "brightness": brightness,
        "threshold": threshold
    })
    return sendCommand(command)

@mcp.tool()
def apply_smart_sharpen(layer_id: int, amount: int = 100, radius: float = 1.0, noise_reduction: int = 0, remove_type: str = "gaussianBlur"):
    """Applies Smart Sharpen filter with advanced control.

    Args:
        layer_id (int): ID of the layer
        amount (int): Sharpening amount (1-500). Default 100.
        radius (float): Radius in pixels (0.1-64). Default 1.0.
        noise_reduction (int): Noise reduction percentage (0-100). Default 0.
        remove_type (str): Type of blur to remove - 'gaussianBlur', 'lensBlur', or 'motionBlur'. Default 'gaussianBlur'.
    """
    command = createCommand("applySmartSharpen", {
        "layerId": layer_id,
        "amount": amount,
        "radius": radius,
        "noiseReduction": noise_reduction,
        "removeType": remove_type
    })
    return sendCommand(command)

@mcp.tool()
def apply_oil_paint(layer_id: int, stylization: float = 4.0, cleanliness: float = 5.0, scale: float = 0.5, bristle_detail: float = 2.0, lighting: bool = True):
    """Applies Oil Paint filter for painterly effects.

    Args:
        layer_id (int): ID of the layer
        stylization (float): Stroke style (0.1-10). Default 4.0.
        cleanliness (float): Stroke smoothness (0.1-10). Default 5.0.
        scale (float): Stroke thickness (0.1-10). Default 0.5.
        bristle_detail (float): Bristle detail (0.1-10). Default 2.0.
        lighting (bool): Enable angular lighting direction. Default True.
    """
    command = createCommand("applyOilPaint", {
        "layerId": layer_id,
        "stylization": stylization,
        "cleanliness": cleanliness,
        "scale": scale,
        "bristleDetail": bristle_detail,
        "lighting": lighting
    })
    return sendCommand(command)

@mcp.tool()
def apply_emboss(layer_id: int, angle: int = 135, height: int = 3, amount: int = 100):
    """Applies Emboss filter for a 3D raised/stamped look.

    Args:
        layer_id (int): ID of the layer
        angle (int): Light source angle (-180 to 180). Default 135.
        height (int): Height of emboss in pixels (1-10). Default 3.
        amount (int): Color amount percentage (1-500). Default 100.
    """
    command = createCommand("applyEmboss", {
        "layerId": layer_id,
        "angle": angle,
        "height": height,
        "amount": amount
    })
    return sendCommand(command)

@mcp.tool()
def apply_find_edges(layer_id: int):
    """Applies Find Edges filter to detect and highlight edges.

    Args:
        layer_id (int): ID of the layer
    """
    command = createCommand("applyFindEdges", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def apply_pixelate(layer_id: int, cell_size: int = 10):
    """Applies Mosaic/Pixelate filter.

    Args:
        layer_id (int): ID of the layer
        cell_size (int): Size of pixelated cells (2-200). Default 10.
    """
    command = createCommand("applyPixelate", {"layerId": layer_id, "cellSize": cell_size})
    return sendCommand(command)

@mcp.tool()
def apply_crystallize(layer_id: int, cell_size: int = 10):
    """Applies Crystallize filter for crystal-like polygon shapes.

    Args:
        layer_id (int): ID of the layer
        cell_size (int): Crystal cell size (3-300). Default 10.
    """
    command = createCommand("applyCrystallize", {"layerId": layer_id, "cellSize": cell_size})
    return sendCommand(command)

@mcp.tool()
def apply_color_halftone(layer_id: int, max_radius: int = 8, angle1: int = 108, angle2: int = 162, angle3: int = 90, angle4: int = 45):
    """Applies Color Halftone filter for comic book / print dot pattern.

    Args:
        layer_id (int): ID of the layer
        max_radius (int): Maximum dot radius in pixels (4-127). Default 8.
        angle1 (int): Screen angle for channel 1 in degrees. Default 108.
        angle2 (int): Screen angle for channel 2 in degrees. Default 162.
        angle3 (int): Screen angle for channel 3 in degrees. Default 90.
        angle4 (int): Screen angle for channel 4 in degrees. Default 45.
    """
    command = createCommand("applyColorHalftone", {
        "layerId": layer_id,
        "maxRadius": max_radius,
        "angle1": angle1,
        "angle2": angle2,
        "angle3": angle3,
        "angle4": angle4
    })
    return sendCommand(command)

@mcp.tool()
def apply_twirl_distortion(layer_id: int, angle: int = 50):
    """Applies Twirl distortion filter.

    Args:
        layer_id (int): ID of the layer
        angle (int): Twirl angle (-999 to 999). Default 50.
    """
    command = createCommand("applyTwirlDistortion", {"layerId": layer_id, "angle": angle})
    return sendCommand(command)

@mcp.tool()
def apply_zig_zag_distortion(layer_id: int, amount: int = 10, ridges: int = 5, style: str = "aroundCenter"):
    """Applies ZigZag distortion filter for ripple/pond effects.

    Args:
        layer_id (int): ID of the layer
        amount (int): Distortion amount (-100 to 100). Default 10.
        ridges (int): Number of ridges (1-20). Default 5.
        style (str): 'aroundCenter', 'outFromCenter', or 'pondRipples'. Default 'aroundCenter'.
    """
    command = createCommand("applyZigZagDistortion", {
        "layerId": layer_id,
        "amount": amount,
        "ridges": ridges,
        "style": style
    })
    return sendCommand(command)

@mcp.tool()
def apply_solarize(layer_id: int):
    """Applies Solarize filter for a photographic solarization effect.

    Args:
        layer_id (int): ID of the layer
    """
    command = createCommand("applySolarize", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def apply_posterize_filter(layer_id: int, levels: int = 4):
    """Applies Posterize filter to reduce tonal levels.

    Args:
        layer_id (int): ID of the layer
        levels (int): Number of tonal levels per channel (2-255). Default 4.
    """
    command = createCommand("applyPosterize", {"layerId": layer_id, "levels": levels})
    return sendCommand(command)

@mcp.tool()
def apply_despeckle(layer_id: int):
    """Applies Despeckle noise reduction filter.

    Args:
        layer_id (int): ID of the layer
    """
    command = createCommand("applyDespeckle", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def apply_median_noise(layer_id: int, radius: int = 1):
    """Applies Median noise reduction filter. Good for removing salt-and-pepper noise.

    Args:
        layer_id (int): ID of the layer
        radius (int): Median radius in pixels (1-100). Default 1.
    """
    command = createCommand("applyMedianNoise", {"layerId": layer_id, "radius": radius})
    return sendCommand(command)

@mcp.tool()
def apply_dust_and_scratches(layer_id: int, radius: int = 1, threshold: int = 0):
    """Applies Dust & Scratches noise reduction filter.

    Args:
        layer_id (int): ID of the layer
        radius (int): Search radius (1-100). Default 1.
        threshold (int): Threshold for noise (0-255). Default 0.
    """
    command = createCommand("applyDustAndScratches", {
        "layerId": layer_id,
        "radius": radius,
        "threshold": threshold
    })
    return sendCommand(command)


# =============================================================================
# ADJUSTMENT LAYERS - New expanded adjustments (12 new)
# =============================================================================

@mcp.tool()
def add_curves_adjustment_layer(layer_id: int, channel: str = "composite", points: list = [{"input": 0, "output": 0}, {"input": 255, "output": 255}]):
    """Adds a Curves adjustment layer for precise tonal control.

    Args:
        layer_id (int): ID of the layer to apply to
        channel (str): Channel to adjust - 'composite', 'red', 'green', or 'blue'. Default 'composite'.
        points (list): List of curve points, each dict with 'input' (0-255) and 'output' (0-255). Default straight line.
    """
    command = createCommand("addCurvesAdjustmentLayer", {
        "layerId": layer_id,
        "channel": channel,
        "points": points
    })
    return sendCommand(command)

@mcp.tool()
def add_levels_adjustment_layer(layer_id: int, channel: str = "composite", input_shadow: int = 0, input_highlight: int = 255, input_midtone: float = 1.0, output_shadow: int = 0, output_highlight: int = 255):
    """Adds a Levels adjustment layer for tonal range adjustment.

    Args:
        layer_id (int): ID of the layer to apply to
        channel (str): Channel - 'composite', 'red', 'green', or 'blue'. Default 'composite'.
        input_shadow (int): Input shadow level (0-253). Default 0.
        input_highlight (int): Input highlight level (2-255). Default 255.
        input_midtone (float): Gamma/midtone value (0.01-9.99). Default 1.0.
        output_shadow (int): Output shadow level (0-255). Default 0.
        output_highlight (int): Output highlight level (0-255). Default 255.
    """
    command = createCommand("addLevelsAdjustmentLayer", {
        "layerId": layer_id,
        "channel": channel,
        "inputShadow": input_shadow,
        "inputHighlight": input_highlight,
        "inputMidtone": input_midtone,
        "outputShadow": output_shadow,
        "outputHighlight": output_highlight
    })
    return sendCommand(command)

@mcp.tool()
def add_hue_saturation_adjustment_layer(layer_id: int, hue: int = 0, saturation: int = 0, lightness: int = 0, colorize: bool = False):
    """Adds a Hue/Saturation adjustment layer.

    Args:
        layer_id (int): ID of the layer to apply to
        hue (int): Hue shift (-180 to 180). Default 0.
        saturation (int): Saturation adjustment (-100 to 100). Default 0.
        lightness (int): Lightness adjustment (-100 to 100). Default 0.
        colorize (bool): Whether to colorize the entire image with the selected hue. Default False.
    """
    command = createCommand("addHueSaturationAdjustmentLayer", {
        "layerId": layer_id,
        "hue": hue,
        "saturation": saturation,
        "lightness": lightness,
        "colorize": colorize
    })
    return sendCommand(command)

@mcp.tool()
def add_photo_filter_adjustment_layer(layer_id: int, color_red: int = 236, color_green: int = 138, color_blue: int = 0, density: int = 25, preserve_luminosity: bool = True):
    """Adds a Photo Filter adjustment layer to apply a color tint like a camera lens filter.

    Args:
        layer_id (int): ID of the layer to apply to
        color_red (int): Red component of filter color (0-255). Default 236.
        color_green (int): Green component (0-255). Default 138.
        color_blue (int): Blue component (0-255). Default 0.
        density (int): Filter density percentage (1-100). Default 25.
        preserve_luminosity (bool): Preserve luminosity. Default True.
    """
    command = createCommand("addPhotoFilterAdjustmentLayer", {
        "layerId": layer_id,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "density": density,
        "preserveLuminosity": preserve_luminosity
    })
    return sendCommand(command)

@mcp.tool()
def add_channel_mixer_adjustment_layer(layer_id: int, output_channel: str = "red", red: int = 100, green: int = 0, blue: int = 0, constant: int = 0, monochrome: bool = False):
    """Adds a Channel Mixer adjustment layer for advanced color control.

    Args:
        layer_id (int): ID of the layer to apply to
        output_channel (str): Output channel to modify - 'red', 'green', or 'blue'. Default 'red'.
        red (int): Red source percentage (-200 to 200). Default 100.
        green (int): Green source percentage (-200 to 200). Default 0.
        blue (int): Blue source percentage (-200 to 200). Default 0.
        constant (int): Constant offset (-200 to 200). Default 0.
        monochrome (bool): Convert to monochrome. Default False.
    """
    command = createCommand("addChannelMixerAdjustmentLayer", {
        "layerId": layer_id,
        "outputChannel": output_channel,
        "red": red,
        "green": green,
        "blue": blue,
        "constant": constant,
        "monochrome": monochrome
    })
    return sendCommand(command)

@mcp.tool()
def add_gradient_map_adjustment_layer(layer_id: int, color_stops: list = [{"location": 0, "color": {"red": 0, "green": 0, "blue": 0}}, {"location": 100, "color": {"red": 255, "green": 255, "blue": 255}}], reverse: bool = False):
    """Adds a Gradient Map adjustment layer that maps luminosity to a gradient.

    Args:
        layer_id (int): ID of the layer to apply to
        color_stops (list): List of gradient color stops with 'location' (0-100) and 'color' (RGB dict). Default black-to-white.
        reverse (bool): Reverse the gradient direction. Default False.
    """
    command = createCommand("addGradientMapAdjustmentLayer", {
        "layerId": layer_id,
        "colorStops": color_stops,
        "reverse": reverse
    })
    return sendCommand(command)

@mcp.tool()
def add_posterize_adjustment_layer(layer_id: int, levels: int = 4):
    """Adds a Posterize adjustment layer to reduce tonal levels.

    Args:
        layer_id (int): ID of the layer to apply to
        levels (int): Number of tonal levels (2-255). Default 4.
    """
    command = createCommand("addPosterizeAdjustmentLayer", {"layerId": layer_id, "levels": levels})
    return sendCommand(command)

@mcp.tool()
def add_threshold_adjustment_layer(layer_id: int, level: int = 128):
    """Adds a Threshold adjustment layer converting image to pure black and white.

    Args:
        layer_id (int): ID of the layer to apply to
        level (int): Threshold level (1-255). Pixels brighter become white, darker become black. Default 128.
    """
    command = createCommand("addThresholdAdjustmentLayer", {"layerId": layer_id, "level": level})
    return sendCommand(command)

@mcp.tool()
def add_selective_color_adjustment_layer(layer_id: int, colors: str = "reds", cyan: int = 0, magenta: int = 0, yellow: int = 0, black: int = 0):
    """Adds a Selective Color adjustment layer to adjust specific color ranges using CMYK sliders.

    Args:
        layer_id (int): ID of the layer to apply to
        colors (str): Target color range - 'reds', 'yellows', 'greens', 'cyans', 'blues', 'magentas', 'whites', 'neutrals', or 'blacks'. Default 'reds'.
        cyan (int): Cyan adjustment (-100 to 100). Default 0.
        magenta (int): Magenta adjustment (-100 to 100). Default 0.
        yellow (int): Yellow adjustment (-100 to 100). Default 0.
        black (int): Black adjustment (-100 to 100). Default 0.
    """
    command = createCommand("addSelectiveColorAdjustmentLayer", {
        "layerId": layer_id,
        "colors": colors,
        "cyan": cyan,
        "magenta": magenta,
        "yellow": yellow,
        "black": black
    })
    return sendCommand(command)

@mcp.tool()
def add_exposure_adjustment_layer(layer_id: int, exposure: float = 0.0, offset: float = 0.0, gamma: float = 1.0):
    """Adds an Exposure adjustment layer for HDR-style tonal control.

    Args:
        layer_id (int): ID of the layer to apply to
        exposure (float): Exposure value (-20.0 to 20.0). Default 0.0.
        offset (float): Shadow offset (-0.5 to 0.5). Default 0.0.
        gamma (float): Gamma correction (0.01 to 9.99). Default 1.0.
    """
    command = createCommand("addExposureAdjustmentLayer", {
        "layerId": layer_id,
        "exposure": exposure,
        "offset": offset,
        "gamma": gamma
    })
    return sendCommand(command)

@mcp.tool()
def add_invert_adjustment_layer(layer_id: int):
    """Adds an Invert adjustment layer that inverts all colors.

    Args:
        layer_id (int): ID of the layer to apply to
    """
    command = createCommand("addInvertAdjustmentLayer", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def add_solid_color_fill_layer(color_red: int = 255, color_green: int = 0, color_blue: int = 0):
    """Creates a Solid Color fill layer.

    Args:
        color_red (int): Red component (0-255). Default 255.
        color_green (int): Green component (0-255). Default 0.
        color_blue (int): Blue component (0-255). Default 0.
    """
    command = createCommand("addSolidColorFillLayer", {
        "color": {"red": color_red, "green": color_green, "blue": color_blue}
    })
    return sendCommand(command)


# =============================================================================
# LAYER STYLES - New expanded styles (8 new)
# =============================================================================

@mcp.tool()
def add_inner_shadow_layer_style(layer_id: int, blend_mode: str = "MULTIPLY", color_red: int = 0, color_green: int = 0, color_blue: int = 0, opacity: int = 75, angle: int = 120, distance: int = 5, choke: int = 0, size: int = 5):
    """Adds an Inner Shadow layer style.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'MULTIPLY'.
        color_red (int): Red (0-255). Default 0.
        color_green (int): Green (0-255). Default 0.
        color_blue (int): Blue (0-255). Default 0.
        opacity (int): Opacity (0-100). Default 75.
        angle (int): Light angle (-180 to 180). Default 120.
        distance (int): Shadow distance in pixels (0-30000). Default 5.
        choke (int): Choke/spread percentage (0-100). Default 0.
        size (int): Blur size in pixels (0-250). Default 5.
    """
    command = createCommand("addInnerShadowLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity,
        "angle": angle,
        "distance": distance,
        "choke": choke,
        "size": size
    })
    return sendCommand(command)

@mcp.tool()
def add_outer_glow_layer_style(layer_id: int, blend_mode: str = "SCREEN", color_red: int = 255, color_green: int = 255, color_blue: int = 190, opacity: int = 75, spread: int = 0, size: int = 5, noise: int = 0):
    """Adds an Outer Glow layer style.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'SCREEN'.
        color_red (int): Red (0-255). Default 255.
        color_green (int): Green (0-255). Default 255.
        color_blue (int): Blue (0-255). Default 190.
        opacity (int): Opacity (0-100). Default 75.
        spread (int): Spread percentage (0-100). Default 0.
        size (int): Blur size in pixels (0-250). Default 5.
        noise (int): Noise percentage (0-100). Default 0.
    """
    command = createCommand("addOuterGlowLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity,
        "spread": spread,
        "size": size,
        "noise": noise
    })
    return sendCommand(command)

@mcp.tool()
def add_inner_glow_layer_style(layer_id: int, blend_mode: str = "SCREEN", color_red: int = 255, color_green: int = 255, color_blue: int = 190, opacity: int = 75, choke: int = 0, size: int = 5, source: str = "edge", noise: int = 0):
    """Adds an Inner Glow layer style.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'SCREEN'.
        color_red (int): Red (0-255). Default 255.
        color_green (int): Green (0-255). Default 255.
        color_blue (int): Blue (0-255). Default 190.
        opacity (int): Opacity (0-100). Default 75.
        choke (int): Choke percentage (0-100). Default 0.
        size (int): Blur size in pixels (0-250). Default 5.
        source (str): Glow source - 'edge' or 'center'. Default 'edge'.
        noise (int): Noise percentage (0-100). Default 0.
    """
    command = createCommand("addInnerGlowLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity,
        "choke": choke,
        "size": size,
        "source": source,
        "noise": noise
    })
    return sendCommand(command)

@mcp.tool()
def add_bevel_emboss_layer_style(
    layer_id: int,
    style: str = "innerBevel",
    technique: str = "smooth",
    depth: int = 100,
    direction: str = "up",
    size: int = 5,
    soften: int = 0,
    angle: int = 120,
    altitude: int = 30,
    highlight_mode: str = "SCREEN",
    highlight_color_red: int = 255,
    highlight_color_green: int = 255,
    highlight_color_blue: int = 255,
    highlight_opacity: int = 75,
    shadow_mode: str = "MULTIPLY",
    shadow_color_red: int = 0,
    shadow_color_green: int = 0,
    shadow_color_blue: int = 0,
    shadow_opacity: int = 75
):
    """Adds a Bevel and Emboss layer style for 3D depth effects.

    Args:
        layer_id (int): ID of the layer
        style (str): Bevel style - 'outerBevel', 'innerBevel', 'emboss', 'pillowEmboss', or 'strokeEmboss'. Default 'innerBevel'.
        technique (str): Technique - 'smooth', 'chiselHard', or 'chiselSoft'. Default 'smooth'.
        depth (int): Depth percentage (1-1000). Default 100.
        direction (str): Light direction - 'up' or 'down'. Default 'up'.
        size (int): Size in pixels (0-250). Default 5.
        soften (int): Soften amount (0-16). Default 0.
        angle (int): Light angle (-180 to 180). Default 120.
        altitude (int): Light altitude (0-90). Default 30.
        highlight_mode (str): Highlight blend mode. Default 'SCREEN'.
        highlight_color_red (int): Highlight red (0-255). Default 255.
        highlight_color_green (int): Highlight green (0-255). Default 255.
        highlight_color_blue (int): Highlight blue (0-255). Default 255.
        highlight_opacity (int): Highlight opacity (0-100). Default 75.
        shadow_mode (str): Shadow blend mode. Default 'MULTIPLY'.
        shadow_color_red (int): Shadow red (0-255). Default 0.
        shadow_color_green (int): Shadow green (0-255). Default 0.
        shadow_color_blue (int): Shadow blue (0-255). Default 0.
        shadow_opacity (int): Shadow opacity (0-100). Default 75.
    """
    command = createCommand("addBevelEmbossLayerStyle", {
        "layerId": layer_id,
        "style": style,
        "technique": technique,
        "depth": depth,
        "direction": direction,
        "size": size,
        "soften": soften,
        "angle": angle,
        "altitude": altitude,
        "highlightMode": highlight_mode,
        "highlightColor": {"red": highlight_color_red, "green": highlight_color_green, "blue": highlight_color_blue},
        "highlightOpacity": highlight_opacity,
        "shadowMode": shadow_mode,
        "shadowColor": {"red": shadow_color_red, "green": shadow_color_green, "blue": shadow_color_blue},
        "shadowOpacity": shadow_opacity
    })
    return sendCommand(command)

@mcp.tool()
def add_satin_layer_style(layer_id: int, blend_mode: str = "MULTIPLY", color_red: int = 0, color_green: int = 0, color_blue: int = 0, opacity: int = 50, angle: int = 19, distance: int = 11, size: int = 14, invert: bool = False):
    """Adds a Satin layer style for silky interior shading.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'MULTIPLY'.
        color_red (int): Red (0-255). Default 0.
        color_green (int): Green (0-255). Default 0.
        color_blue (int): Blue (0-255). Default 0.
        opacity (int): Opacity (0-100). Default 50.
        angle (int): Angle (-180 to 180). Default 19.
        distance (int): Distance in pixels (0-30000). Default 11.
        size (int): Size in pixels (0-250). Default 14.
        invert (bool): Invert the effect. Default False.
    """
    command = createCommand("addSatinLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity,
        "angle": angle,
        "distance": distance,
        "size": size,
        "invert": invert
    })
    return sendCommand(command)

@mcp.tool()
def add_color_overlay_layer_style(layer_id: int, blend_mode: str = "NORMAL", color_red: int = 255, color_green: int = 0, color_blue: int = 0, opacity: int = 100):
    """Adds a Color Overlay layer style.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'NORMAL'.
        color_red (int): Red (0-255). Default 255.
        color_green (int): Green (0-255). Default 0.
        color_blue (int): Blue (0-255). Default 0.
        opacity (int): Opacity (0-100). Default 100.
    """
    command = createCommand("addColorOverlayLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity
    })
    return sendCommand(command)

@mcp.tool()
def add_gradient_overlay_layer_style(
    layer_id: int,
    blend_mode: str = "NORMAL",
    opacity: int = 100,
    angle: int = 90,
    scale: int = 100,
    gradient_type: str = "linear",
    color_stops: list = [{"location": 0, "color": {"red": 0, "green": 0, "blue": 0}}, {"location": 100, "color": {"red": 255, "green": 255, "blue": 255}}],
    opacity_stops: list = [{"location": 0, "opacity": 100}, {"location": 100, "opacity": 100}],
    reverse: bool = False
):
    """Adds a Gradient Overlay layer style.

    Args:
        layer_id (int): ID of the layer
        blend_mode (str): Blend mode. Default 'NORMAL'.
        opacity (int): Opacity (0-100). Default 100.
        angle (int): Gradient angle (-180 to 180). Default 90.
        scale (int): Gradient scale percentage (10-150). Default 100.
        gradient_type (str): Type - 'linear', 'radial', 'angle', 'reflected', or 'diamond'. Default 'linear'.
        color_stops (list): Color stops with 'location' (0-100) and 'color' RGB dict.
        opacity_stops (list): Opacity stops with 'location' (0-100) and 'opacity' (0-100).
        reverse (bool): Reverse gradient. Default False.
    """
    command = createCommand("addGradientOverlayLayerStyle", {
        "layerId": layer_id,
        "blendMode": blend_mode,
        "opacity": opacity,
        "angle": angle,
        "scale": scale,
        "type": gradient_type,
        "colorStops": color_stops,
        "opacityStops": opacity_stops,
        "reverse": reverse
    })
    return sendCommand(command)

@mcp.tool()
def clear_layer_styles(layer_id: int):
    """Removes all layer styles from the specified layer.

    Args:
        layer_id (int): ID of the layer to clear styles from
    """
    command = createCommand("clearLayerStyles", {"layerId": layer_id})
    return sendCommand(command)


# =============================================================================
# TRANSFORMS (5 new)
# =============================================================================

@mcp.tool()
def free_transform(layer_id: int, width: int = 100, height: int = 100, angle: int = 0, skew_x: int = 0, skew_y: int = 0, move_x: int = 0, move_y: int = 0):
    """Applies a free transform to the layer with combined scale, rotation, skew and move.

    Args:
        layer_id (int): ID of the layer
        width (int): Horizontal scale percentage. Default 100.
        height (int): Vertical scale percentage. Default 100.
        angle (int): Rotation angle in degrees (-359 to 359). Default 0.
        skew_x (int): Horizontal skew in degrees (-89 to 89). Default 0.
        skew_y (int): Vertical skew in degrees (-89 to 89). Default 0.
        move_x (int): Horizontal move in pixels. Default 0.
        move_y (int): Vertical move in pixels. Default 0.
    """
    command = createCommand("freeTransform", {
        "layerId": layer_id,
        "width": width,
        "height": height,
        "angle": angle,
        "skewX": skew_x,
        "skewY": skew_y,
        "moveX": move_x,
        "moveY": move_y
    })
    return sendCommand(command)

@mcp.tool()
def perspective_transform(layer_id: int, top_left_x: int = 0, top_left_y: int = 0, top_right_x: int = 100, top_right_y: int = 0, bottom_right_x: int = 100, bottom_right_y: int = 100, bottom_left_x: int = 0, bottom_left_y: int = 100):
    """Applies a perspective transform by moving the four corners of the layer.

    Args:
        layer_id (int): ID of the layer
        top_left_x (int): X offset of the top-left corner. Default 0.
        top_left_y (int): Y offset of the top-left corner. Default 0.
        top_right_x (int): X offset of the top-right corner. Default 100.
        top_right_y (int): Y offset of the top-right corner. Default 0.
        bottom_right_x (int): X offset of the bottom-right corner. Default 100.
        bottom_right_y (int): Y offset of the bottom-right corner. Default 100.
        bottom_left_x (int): X offset of the bottom-left corner. Default 0.
        bottom_left_y (int): Y offset of the bottom-left corner. Default 100.
    """
    command = createCommand("perspectiveTransform", {
        "layerId": layer_id,
        "topLeft": {"x": top_left_x, "y": top_left_y},
        "topRight": {"x": top_right_x, "y": top_right_y},
        "bottomRight": {"x": bottom_right_x, "y": bottom_right_y},
        "bottomLeft": {"x": bottom_left_x, "y": bottom_left_y}
    })
    return sendCommand(command)

@mcp.tool()
def warp_transform(layer_id: int, warp_style: str = "arc", bend: int = 50, horizontal_distortion: int = 0, vertical_distortion: int = 0):
    """Applies a warp transform to the layer.

    Args:
        layer_id (int): ID of the layer
        warp_style (str): Warp preset style. Valid values: 'arc', 'arcLower', 'arcUpper', 'arch', 'bulge', 'shellLower', 'shellUpper', 'flag', 'wave', 'fish', 'rise', 'fisheye', 'inflate', 'squeeze', 'twist'. Default 'arc'.
        bend (int): Bend amount (-100 to 100). Default 50.
        horizontal_distortion (int): Horizontal distortion (-100 to 100). Default 0.
        vertical_distortion (int): Vertical distortion (-100 to 100). Default 0.
    """
    command = createCommand("warpTransform", {
        "layerId": layer_id,
        "warpStyle": warp_style,
        "bend": bend,
        "horizontalDistortion": horizontal_distortion,
        "verticalDistortion": vertical_distortion
    })
    return sendCommand(command)

@mcp.tool()
def content_aware_scale(layer_id: int, width: int = 100, height: int = 100):
    """Applies Content-Aware Scale which intelligently resizes while protecting important content.

    Args:
        layer_id (int): ID of the layer
        width (int): Target width as percentage. Default 100.
        height (int): Target height as percentage. Default 100.
    """
    command = createCommand("contentAwareScale", {
        "layerId": layer_id,
        "width": width,
        "height": height
    })
    return sendCommand(command)

@mcp.tool()
def convert_to_smart_object(layer_id: int):
    """Converts the specified layer to a Smart Object.

    Args:
        layer_id (int): ID of the layer to convert
    """
    command = createCommand("convertToSmartObject", {"layerId": layer_id})
    return sendCommand(command)


# =============================================================================
# SHAPES (5 new)
# =============================================================================

@mcp.tool()
def draw_rectangle_shape(top: int = 0, left: int = 0, bottom: int = 100, right: int = 100, fill_color_red: int = 255, fill_color_green: int = 0, fill_color_blue: int = 0, stroke_color_red: int = 0, stroke_color_green: int = 0, stroke_color_blue: int = 0, stroke_width: int = 0, corner_radius: int = 0):
    """Draws a rectangle shape on a new shape layer.

    Args:
        top (int): Top bound. Default 0.
        left (int): Left bound. Default 0.
        bottom (int): Bottom bound. Default 100.
        right (int): Right bound. Default 100.
        fill_color_red (int): Fill red (0-255). Default 255.
        fill_color_green (int): Fill green (0-255). Default 0.
        fill_color_blue (int): Fill blue (0-255). Default 0.
        stroke_color_red (int): Stroke red (0-255). Default 0.
        stroke_color_green (int): Stroke green (0-255). Default 0.
        stroke_color_blue (int): Stroke blue (0-255). Default 0.
        stroke_width (int): Stroke width in pixels (0 = no stroke). Default 0.
        corner_radius (int): Corner radius for rounded rectangles (0 = sharp). Default 0.
    """
    command = createCommand("drawRectangleShape", {
        "bounds": {"top": top, "left": left, "bottom": bottom, "right": right},
        "fillColor": {"red": fill_color_red, "green": fill_color_green, "blue": fill_color_blue},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width,
        "cornerRadius": corner_radius
    })
    return sendCommand(command)

@mcp.tool()
def draw_ellipse_shape(top: int = 0, left: int = 0, bottom: int = 100, right: int = 100, fill_color_red: int = 255, fill_color_green: int = 0, fill_color_blue: int = 0, stroke_color_red: int = 0, stroke_color_green: int = 0, stroke_color_blue: int = 0, stroke_width: int = 0):
    """Draws an ellipse shape on a new shape layer.

    Args:
        top (int): Top bound. Default 0.
        left (int): Left bound. Default 0.
        bottom (int): Bottom bound. Default 100.
        right (int): Right bound. Default 100.
        fill_color_red (int): Fill red (0-255). Default 255.
        fill_color_green (int): Fill green (0-255). Default 0.
        fill_color_blue (int): Fill blue (0-255). Default 0.
        stroke_color_red (int): Stroke red (0-255). Default 0.
        stroke_color_green (int): Stroke green (0-255). Default 0.
        stroke_color_blue (int): Stroke blue (0-255). Default 0.
        stroke_width (int): Stroke width in pixels (0 = no stroke). Default 0.
    """
    command = createCommand("drawEllipseShape", {
        "bounds": {"top": top, "left": left, "bottom": bottom, "right": right},
        "fillColor": {"red": fill_color_red, "green": fill_color_green, "blue": fill_color_blue},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width
    })
    return sendCommand(command)

@mcp.tool()
def draw_line_shape(start_x: int = 0, start_y: int = 0, end_x: int = 100, end_y: int = 100, stroke_color_red: int = 255, stroke_color_green: int = 255, stroke_color_blue: int = 255, stroke_width: int = 2):
    """Draws a line shape on a new shape layer.

    Args:
        start_x (int): Starting X coordinate. Default 0.
        start_y (int): Starting Y coordinate. Default 0.
        end_x (int): Ending X coordinate. Default 100.
        end_y (int): Ending Y coordinate. Default 100.
        stroke_color_red (int): Line red (0-255). Default 255.
        stroke_color_green (int): Line green (0-255). Default 255.
        stroke_color_blue (int): Line blue (0-255). Default 255.
        stroke_width (int): Line width in pixels. Default 2.
    """
    command = createCommand("drawLineShape", {
        "startPoint": {"x": start_x, "y": start_y},
        "endPoint": {"x": end_x, "y": end_y},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width
    })
    return sendCommand(command)

@mcp.tool()
def draw_arrow_shape(start_x: int = 0, start_y: int = 0, end_x: int = 100, end_y: int = 100, stroke_color_red: int = 255, stroke_color_green: int = 255, stroke_color_blue: int = 255, stroke_width: int = 2, head_size: int = 12):
    """Draws an arrow shape (line with arrowhead) on a new shape layer.

    Args:
        start_x (int): Starting X coordinate. Default 0.
        start_y (int): Starting Y coordinate. Default 0.
        end_x (int): Ending X coordinate (arrow tip). Default 100.
        end_y (int): Ending Y coordinate (arrow tip). Default 100.
        stroke_color_red (int): Arrow red (0-255). Default 255.
        stroke_color_green (int): Arrow green (0-255). Default 255.
        stroke_color_blue (int): Arrow blue (0-255). Default 255.
        stroke_width (int): Line width in pixels. Default 2.
        head_size (int): Arrowhead size in pixels. Default 12.
    """
    command = createCommand("drawArrowShape", {
        "startPoint": {"x": start_x, "y": start_y},
        "endPoint": {"x": end_x, "y": end_y},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width,
        "headSize": head_size
    })
    return sendCommand(command)

@mcp.tool()
def draw_polygon_shape(sides: int = 6, center_x: int = 100, center_y: int = 100, radius: int = 50, fill_color_red: int = 255, fill_color_green: int = 0, fill_color_blue: int = 0, stroke_color_red: int = 0, stroke_color_green: int = 0, stroke_color_blue: int = 0, stroke_width: int = 0):
    """Draws a regular polygon shape (triangle, pentagon, hexagon, etc.).

    Args:
        sides (int): Number of sides (3-100). Default 6.
        center_x (int): Center X coordinate. Default 100.
        center_y (int): Center Y coordinate. Default 100.
        radius (int): Radius in pixels. Default 50.
        fill_color_red (int): Fill red (0-255). Default 255.
        fill_color_green (int): Fill green (0-255). Default 0.
        fill_color_blue (int): Fill blue (0-255). Default 0.
        stroke_color_red (int): Stroke red (0-255). Default 0.
        stroke_color_green (int): Stroke green (0-255). Default 0.
        stroke_color_blue (int): Stroke blue (0-255). Default 0.
        stroke_width (int): Stroke width (0 = no stroke). Default 0.
    """
    command = createCommand("drawPolygonShape", {
        "sides": sides,
        "centerX": center_x,
        "centerY": center_y,
        "radius": radius,
        "fillColor": {"red": fill_color_red, "green": fill_color_green, "blue": fill_color_blue},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width
    })
    return sendCommand(command)

@mcp.tool()
def draw_custom_path(points: list = [{"x": 0, "y": 0}, {"x": 100, "y": 50}, {"x": 0, "y": 100}], closed: bool = True, fill_color_red: int = 255, fill_color_green: int = 0, fill_color_blue: int = 0, stroke_color_red: int = 0, stroke_color_green: int = 0, stroke_color_blue: int = 0, stroke_width: int = 0):
    """Draws a custom vector path shape. Points can include bezier curve handles.

    Args:
        points (list): List of path point dicts. Simple points: {"x": 0, "y": 0}. Bezier points: {"x": 0, "y": 0, "handleInX": -10, "handleInY": 0, "handleOutX": 10, "handleOutY": 0}.
        closed (bool): Whether path is closed. Default True.
        fill_color_red (int): Fill red (0-255). Default 255.
        fill_color_green (int): Fill green (0-255). Default 0.
        fill_color_blue (int): Fill blue (0-255). Default 0.
        stroke_color_red (int): Stroke red (0-255). Default 0.
        stroke_color_green (int): Stroke green (0-255). Default 0.
        stroke_color_blue (int): Stroke blue (0-255). Default 0.
        stroke_width (int): Stroke width (0 = no stroke). Default 0.
    """
    command = createCommand("drawCustomPath", {
        "points": points,
        "closed": closed,
        "fillColor": {"red": fill_color_red, "green": fill_color_green, "blue": fill_color_blue},
        "strokeColor": {"red": stroke_color_red, "green": stroke_color_green, "blue": stroke_color_blue},
        "strokeWidth": stroke_width
    })
    return sendCommand(command)


# =============================================================================
# PAINTING (4 new)
# =============================================================================

@mcp.tool()
def brush_stroke(layer_id: int, points: list = [{"x": 0, "y": 0}, {"x": 100, "y": 100}], brush_size: int = 10, color_red: int = 255, color_green: int = 255, color_blue: int = 255, opacity: int = 100, hardness: int = 100, flow: int = 100):
    """Paints a brush stroke along the specified path of points on the given layer.

    Args:
        layer_id (int): ID of the pixel layer to paint on
        points (list): List of {x, y} point dicts defining the stroke path.
        brush_size (int): Brush diameter in pixels (1-5000). Default 10.
        color_red (int): Brush red (0-255). Default 255.
        color_green (int): Brush green (0-255). Default 255.
        color_blue (int): Brush blue (0-255). Default 255.
        opacity (int): Brush opacity (1-100). Default 100.
        hardness (int): Brush hardness (0-100). Default 100.
        flow (int): Brush flow (1-100). Default 100.
    """
    command = createCommand("brushStroke", {
        "layerId": layer_id,
        "points": points,
        "brushSize": brush_size,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "opacity": opacity,
        "hardness": hardness,
        "flow": flow
    })
    return sendCommand(command)

@mcp.tool()
def eraser_stroke(layer_id: int, points: list = [{"x": 0, "y": 0}, {"x": 100, "y": 100}], brush_size: int = 10, opacity: int = 100, hardness: int = 100):
    """Erases along the specified path of points on the given layer.

    Args:
        layer_id (int): ID of the pixel layer to erase on
        points (list): List of {x, y} point dicts defining the eraser path.
        brush_size (int): Eraser size in pixels (1-5000). Default 10.
        opacity (int): Eraser opacity (1-100). Default 100.
        hardness (int): Eraser hardness (0-100). Default 100.
    """
    command = createCommand("eraserStroke", {
        "layerId": layer_id,
        "points": points,
        "brushSize": brush_size,
        "opacity": opacity,
        "hardness": hardness
    })
    return sendCommand(command)

@mcp.tool()
def gradient_draw(layer_id: int, start_x: int = 0, start_y: int = 0, end_x: int = 100, end_y: int = 100, gradient_type: str = "linear", color_stops: list = [{"location": 0, "color": {"red": 0, "green": 0, "blue": 0}}, {"location": 100, "color": {"red": 255, "green": 255, "blue": 255}}], opacity: int = 100):
    """Draws a gradient directly on the specified pixel layer.

    Args:
        layer_id (int): ID of the pixel layer
        start_x (int): Start X coordinate. Default 0.
        start_y (int): Start Y coordinate. Default 0.
        end_x (int): End X coordinate. Default 100.
        end_y (int): End Y coordinate. Default 100.
        gradient_type (str): Type - 'linear', 'radial', 'angle', 'reflected', or 'diamond'. Default 'linear'.
        color_stops (list): Color stops with 'location' (0-100) and 'color' RGB dict.
        opacity (int): Gradient opacity (1-100). Default 100.
    """
    command = createCommand("gradientDraw", {
        "layerId": layer_id,
        "startPoint": {"x": start_x, "y": start_y},
        "endPoint": {"x": end_x, "y": end_y},
        "gradientType": gradient_type,
        "colorStops": color_stops,
        "opacity": opacity
    })
    return sendCommand(command)

@mcp.tool()
def paint_bucket_fill(layer_id: int, x: int = 0, y: int = 0, color_red: int = 255, color_green: int = 0, color_blue: int = 0, tolerance: int = 32, contiguous: bool = True, opacity: int = 100):
    """Fills an area with color using the Paint Bucket tool (flood fill).

    Args:
        layer_id (int): ID of the pixel layer
        x (int): X coordinate of the fill origin. Default 0.
        y (int): Y coordinate of the fill origin. Default 0.
        color_red (int): Fill red (0-255). Default 255.
        color_green (int): Fill green (0-255). Default 0.
        color_blue (int): Fill blue (0-255). Default 0.
        tolerance (int): Color tolerance (0-255). Default 32.
        contiguous (bool): Fill only contiguous pixels. Default True.
        opacity (int): Fill opacity (1-100). Default 100.
    """
    command = createCommand("paintBucketFill", {
        "layerId": layer_id,
        "x": x,
        "y": y,
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "tolerance": tolerance,
        "contiguous": contiguous,
        "opacity": opacity
    })
    return sendCommand(command)


# =============================================================================
# ADVANCED OPERATIONS (10 new)
# =============================================================================

@mcp.tool()
def content_aware_fill():
    """Performs Content-Aware Fill on the active selection. Requires an active selection.
    Intelligently fills the selected area using surrounding content.
    """
    command = createCommand("contentAwareFill", {})
    return sendCommand(command)

@mcp.tool()
def auto_tone():
    """Applies Auto Tone adjustment to the active document for automatic tonal correction."""
    command = createCommand("autoTone", {})
    return sendCommand(command)

@mcp.tool()
def auto_color():
    """Applies Auto Color adjustment to the active document for automatic color correction."""
    command = createCommand("autoColor", {})
    return sendCommand(command)

@mcp.tool()
def auto_contrast():
    """Applies Auto Contrast adjustment to the active document for automatic contrast correction."""
    command = createCommand("autoContrast", {})
    return sendCommand(command)

@mcp.tool()
def shadows_highlights(layer_id: int, shadow_amount: int = 35, shadow_tonal_width: int = 50, shadow_radius: int = 30, highlight_amount: int = 0, highlight_tonal_width: int = 50, highlight_radius: int = 30, color_correction: int = 20, midtone_contrast: int = 0):
    """Applies Shadows/Highlights adjustment for recovering shadow and highlight detail.

    Args:
        layer_id (int): ID of the layer
        shadow_amount (int): Shadow lightening amount (0-100). Default 35.
        shadow_tonal_width (int): Shadow tonal range (0-100). Default 50.
        shadow_radius (int): Shadow radius (0-2500). Default 30.
        highlight_amount (int): Highlight darkening amount (0-100). Default 0.
        highlight_tonal_width (int): Highlight tonal range (0-100). Default 50.
        highlight_radius (int): Highlight radius (0-2500). Default 30.
        color_correction (int): Color correction (-100 to 100). Default 20.
        midtone_contrast (int): Midtone contrast (-100 to 100). Default 0.
    """
    command = createCommand("shadowsHighlights", {
        "layerId": layer_id,
        "shadowAmount": shadow_amount,
        "shadowTonalWidth": shadow_tonal_width,
        "shadowRadius": shadow_radius,
        "highlightAmount": highlight_amount,
        "highlightTonalWidth": highlight_tonal_width,
        "highlightRadius": highlight_radius,
        "colorCorrection": color_correction,
        "midtoneContrast": midtone_contrast
    })
    return sendCommand(command)

@mcp.tool()
def lens_correction(layer_id: int, distortion: int = 0, vignette: int = 0, vignette_midpoint: int = 50, chromatic_aberration_rg: int = 0, chromatic_aberration_by: int = 0):
    """Applies manual Lens Correction to fix distortion, vignette, and chromatic aberration.

    Args:
        layer_id (int): ID of the layer
        distortion (int): Barrel/pincushion distortion (-100 to 100). Default 0.
        vignette (int): Vignette amount (-100 to 100). Default 0.
        vignette_midpoint (int): Vignette midpoint (0-100). Default 50.
        chromatic_aberration_rg (int): Red/Green fringe fix (-100 to 100). Default 0.
        chromatic_aberration_by (int): Blue/Yellow fringe fix (-100 to 100). Default 0.
    """
    command = createCommand("lensCorrection", {
        "layerId": layer_id,
        "distortion": distortion,
        "vignette": vignette,
        "vignetteMidpoint": vignette_midpoint,
        "chromaticAberrationRG": chromatic_aberration_rg,
        "chromaticAberrationBY": chromatic_aberration_by
    })
    return sendCommand(command)

@mcp.tool()
def liquify_forward(layer_id: int, start_x: int = 50, start_y: int = 50, end_x: int = 100, end_y: int = 100, brush_size: int = 64, pressure: int = 50):
    """Applies a forward warp Liquify push from start point to end point.

    Note: This is a simplified liquify that pushes pixels in a straight line. For complex liquify operations, use Photoshop directly.

    Args:
        layer_id (int): ID of the layer
        start_x (int): Start X coordinate. Default 50.
        start_y (int): Start Y coordinate. Default 50.
        end_x (int): End X coordinate. Default 100.
        end_y (int): End Y coordinate. Default 100.
        brush_size (int): Brush diameter (1-15000). Default 64.
        pressure (int): Warp pressure (1-100). Default 50.
    """
    command = createCommand("liquifyForward", {
        "layerId": layer_id,
        "startX": start_x,
        "startY": start_y,
        "endX": end_x,
        "endY": end_y,
        "brushSize": brush_size,
        "pressure": pressure
    })
    return sendCommand(command)

@mcp.tool()
def apply_displace(layer_id: int, horizontal_scale: int = 10, vertical_scale: int = 10, stretch_to_fit: bool = True, wrap_around: bool = True):
    """Applies Displace distortion filter.

    Args:
        layer_id (int): ID of the layer
        horizontal_scale (int): Horizontal displacement (-999 to 999). Default 10.
        vertical_scale (int): Vertical displacement (-999 to 999). Default 10.
        stretch_to_fit (bool): Stretch displacement map to fit. Default True.
        wrap_around (bool): Wrap undefined areas around. Default True.
    """
    command = createCommand("applyDisplace", {
        "layerId": layer_id,
        "horizontalScale": horizontal_scale,
        "verticalScale": vertical_scale,
        "stretchToFit": stretch_to_fit,
        "wrapAround": wrap_around
    })
    return sendCommand(command)

@mcp.tool()
def apply_sphere(layer_id: int, amount: int = 100, mode: str = "normal"):
    """Applies Spherize distortion filter.

    Args:
        layer_id (int): ID of the layer
        amount (int): Spherize amount (-100 to 100). Default 100.
        mode (str): Mode - 'normal', 'horizontal', or 'vertical'. Default 'normal'.
    """
    command = createCommand("applySphere", {
        "layerId": layer_id,
        "amount": amount,
        "mode": mode
    })
    return sendCommand(command)

@mcp.tool()
def apply_wave(layer_id: int, generators: int = 5, wavelength_min: int = 10, wavelength_max: int = 120, amplitude_min: int = 5, amplitude_max: int = 35, scale_horizontal: int = 100, scale_vertical: int = 100, wave_type: str = "sine"):
    """Applies Wave distortion filter.

    Args:
        layer_id (int): ID of the layer
        generators (int): Number of wave generators (1-999). Default 5.
        wavelength_min (int): Minimum wavelength (1-998). Default 10.
        wavelength_max (int): Maximum wavelength (2-999). Default 120.
        amplitude_min (int): Minimum amplitude (1-998). Default 5.
        amplitude_max (int): Maximum amplitude (2-999). Default 35.
        scale_horizontal (int): Horizontal scale percentage (1-100). Default 100.
        scale_vertical (int): Vertical scale percentage (1-100). Default 100.
        wave_type (str): Wave type - 'sine', 'triangle', or 'square'. Default 'sine'.
    """
    command = createCommand("applyWave", {
        "layerId": layer_id,
        "generators": generators,
        "wavelengthMin": wavelength_min,
        "wavelengthMax": wavelength_max,
        "amplitudeMin": amplitude_min,
        "amplitudeMax": amplitude_max,
        "scaleHorizontal": scale_horizontal,
        "scaleVertical": scale_vertical,
        "waveType": wave_type
    })
    return sendCommand(command)


# =============================================================================
# CHANNELS / SELECTION OPERATIONS (14 new)
# =============================================================================

@mcp.tool()
def select_all():
    """Selects all pixels in the active document (Select > All)."""
    command = createCommand("selectAll", {})
    return sendCommand(command)

@mcp.tool()
def select_color_range(color_red: int = 255, color_green: int = 0, color_blue: int = 0, fuzziness: int = 40):
    """Selects pixels by color range (Select > Color Range).

    Args:
        color_red (int): Target red (0-255). Default 255.
        color_green (int): Target green (0-255). Default 0.
        color_blue (int): Target blue (0-255). Default 0.
        fuzziness (int): Color tolerance (0-200). Default 40.
    """
    command = createCommand("selectColorRange", {
        "color": {"red": color_red, "green": color_green, "blue": color_blue},
        "fuzziness": fuzziness
    })
    return sendCommand(command)

@mcp.tool()
def select_focus_area(fuzziness: int = 50):
    """Selects in-focus areas of the image (Select > Focus Area).

    Args:
        fuzziness (int): Focus range tolerance (0-255). Default 50.
    """
    command = createCommand("selectFocusArea", {"fuzziness": fuzziness})
    return sendCommand(command)

@mcp.tool()
def grow_selection():
    """Grows the current selection to include adjacent similar pixels (Select > Grow)."""
    command = createCommand("growSelection", {})
    return sendCommand(command)

@mcp.tool()
def similar_selection():
    """Selects all similar pixels throughout the image (Select > Similar)."""
    command = createCommand("similarSelection", {})
    return sendCommand(command)

@mcp.tool()
def expand_selection(pixels: int = 1):
    """Expands the current selection by the specified number of pixels.

    Args:
        pixels (int): Number of pixels to expand (1-100). Default 1.
    """
    command = createCommand("expandSelection", {"pixels": pixels})
    return sendCommand(command)

@mcp.tool()
def contract_selection(pixels: int = 1):
    """Contracts the current selection by the specified number of pixels.

    Args:
        pixels (int): Number of pixels to contract (1-100). Default 1.
    """
    command = createCommand("contractSelection", {"pixels": pixels})
    return sendCommand(command)

@mcp.tool()
def feather_selection(pixels: float = 1.0):
    """Feathers (softens) the edges of the current selection.

    Args:
        pixels (float): Feather radius in pixels (0.1-1000). Default 1.0.
    """
    command = createCommand("featherSelection", {"pixels": pixels})
    return sendCommand(command)

@mcp.tool()
def smooth_selection(sample_radius: int = 1):
    """Smooths the current selection edges.

    Args:
        sample_radius (int): Smooth radius (1-100). Default 1.
    """
    command = createCommand("smoothSelection", {"sampleRadius": sample_radius})
    return sendCommand(command)

@mcp.tool()
def border_selection(width: int = 1):
    """Creates a border selection from the current selection.

    Args:
        width (int): Border width in pixels (1-200). Default 1.
    """
    command = createCommand("borderSelection", {"width": width})
    return sendCommand(command)

@mcp.tool()
def save_selection_as_channel(channel_name: str = "Alpha 1"):
    """Saves the current selection as an alpha channel.

    Args:
        channel_name (str): Name for the new channel. Default 'Alpha 1'.
    """
    command = createCommand("saveSelectionAsChannel", {"channelName": channel_name})
    return sendCommand(command)

@mcp.tool()
def load_selection_from_channel(channel_name: str = "Alpha 1"):
    """Loads a selection from a saved alpha channel.

    Args:
        channel_name (str): Name of the channel to load. Default 'Alpha 1'.
    """
    command = createCommand("loadSelectionFromChannel", {"channelName": channel_name})
    return sendCommand(command)

@mcp.tool()
def delete_channel(channel_name: str):
    """Deletes an alpha channel by name.

    Args:
        channel_name (str): Name of the channel to delete.
    """
    command = createCommand("deleteChannel", {"channelName": channel_name})
    return sendCommand(command)

@mcp.tool()
def transform_selection(width: int = 100, height: int = 100, angle: int = 0):
    """Transforms the current selection without affecting pixels.

    Args:
        width (int): Width scale percentage. Default 100.
        height (int): Height scale percentage. Default 100.
        angle (int): Rotation angle in degrees. Default 0.
    """
    command = createCommand("transformSelection", {
        "width": width,
        "height": height,
        "angle": angle
    })
    return sendCommand(command)


# =============================================================================
# DOCUMENT OPERATIONS - New core operations (11 new)
# =============================================================================

@mcp.tool()
def resize_image(width: int = 0, height: int = 0, resolution: int = 0, interpolation: str = "AUTOMATIC", constrain: bool = True):
    """Resizes the entire document image (Image > Image Size).

    Args:
        width (int): New width in pixels (0 = keep current). Default 0.
        height (int): New height in pixels (0 = keep current). Default 0.
        resolution (int): New resolution in PPI (0 = keep current). Default 0.
        interpolation (str): Resampling method. Default 'AUTOMATIC'.
        constrain (bool): Maintain aspect ratio. Default True.
    """
    command = createCommand("resizeImage", {
        "width": width,
        "height": height,
        "resolution": resolution,
        "interpolation": interpolation,
        "constrain": constrain
    })
    return sendCommand(command)

@mcp.tool()
def resize_canvas(width: int = 0, height: int = 0, anchor: str = "MIDDLECENTER", color_red: int = 0, color_green: int = 0, color_blue: int = 0):
    """Resizes the canvas (Image > Canvas Size) without scaling content.

    Args:
        width (int): New canvas width in pixels. Default 0 (keep current).
        height (int): New canvas height in pixels. Default 0 (keep current).
        anchor (str): Anchor position for content placement. Default 'MIDDLECENTER'.
        color_red (int): Canvas extension red (0-255). Default 0.
        color_green (int): Canvas extension green (0-255). Default 0.
        color_blue (int): Canvas extension blue (0-255). Default 0.
    """
    command = createCommand("resizeCanvas", {
        "width": width,
        "height": height,
        "anchor": anchor,
        "color": {"red": color_red, "green": color_green, "blue": color_blue}
    })
    return sendCommand(command)

@mcp.tool()
def rotate_canvas(angle: float = 90.0):
    """Rotates the entire canvas (Image > Image Rotation).

    Args:
        angle (float): Rotation angle. Common values: 90, 180, 270, or arbitrary (-359 to 359). Default 90.
    """
    command = createCommand("rotateCanvas", {"angle": angle})
    return sendCommand(command)

@mcp.tool()
def trim_document(trim_type: str = "transparent", top: bool = True, left: bool = True, bottom: bool = True, right: bool = True):
    """Trims the document by removing surrounding transparent or colored pixels.

    Args:
        trim_type (str): What to trim - 'transparent', 'topLeftPixelColor', or 'bottomRightPixelColor'. Default 'transparent'.
        top (bool): Trim from top. Default True.
        left (bool): Trim from left. Default True.
        bottom (bool): Trim from bottom. Default True.
        right (bool): Trim from right. Default True.
    """
    command = createCommand("trimDocument", {
        "trimType": trim_type,
        "top": top,
        "left": left,
        "bottom": bottom,
        "right": right
    })
    return sendCommand(command)

@mcp.tool()
def reveal_all():
    """Reveals all hidden canvas content by expanding the canvas to fit all layers (Image > Reveal All)."""
    command = createCommand("revealAll", {})
    return sendCommand(command)

@mcp.tool()
def merge_visible():
    """Merges all visible layers into a single layer (Layer > Merge Visible)."""
    command = createCommand("mergeVisible", {})
    return sendCommand(command)

@mcp.tool()
def merge_down(layer_id: int):
    """Merges the specified layer with the layer below it.

    Args:
        layer_id (int): ID of the layer to merge down
    """
    command = createCommand("mergeDown", {"layerId": layer_id})
    return sendCommand(command)

@mcp.tool()
def stamp_visible():
    """Creates a new layer with a merged copy of all visible layers (Ctrl+Shift+Alt+E)."""
    command = createCommand("stampVisible", {})
    return sendCommand(command)

@mcp.tool()
def set_foreground_color(red: int = 0, green: int = 0, blue: int = 0):
    """Sets the foreground color in the toolbar.

    Args:
        red (int): Red (0-255). Default 0.
        green (int): Green (0-255). Default 0.
        blue (int): Blue (0-255). Default 0.
    """
    command = createCommand("setForegroundColor", {"color": {"red": red, "green": green, "blue": blue}})
    return sendCommand(command)

@mcp.tool()
def set_background_color(red: int = 255, green: int = 255, blue: int = 255):
    """Sets the background color in the toolbar.

    Args:
        red (int): Red (0-255). Default 255.
        green (int): Green (0-255). Default 255.
        blue (int): Blue (0-255). Default 255.
    """
    command = createCommand("setBackgroundColor", {"color": {"red": red, "green": green, "blue": blue}})
    return sendCommand(command)

@mcp.tool()
def swap_colors():
    """Swaps the foreground and background colors (X key shortcut)."""
    command = createCommand("swapColors", {})
    return sendCommand(command)


# =============================================================================
# RESOURCE - Instructions for AI
# =============================================================================

@mcp.resource("config://get_instructions")
def get_instructions() -> str:
    """Read this first! Returns information and instructions on how to use Photoshop and this API"""

    return f"""
    You are a photoshop expert who is creative and loves to help other people learn to use Photoshop and create. You are well versed in composition, design and color theory, and try to follow that theory when making decisions.

    Unless otherwise specified, all commands act on the currently active document in Photoshop

    Rules to follow:

    1. Think deeply about how to solve the task
    2. Always check your work
    3. You can view the current visible photoshop file by calling get_document_image
    4. Pay attention to font size (dont make it too big)
    5. Always use alignment (align_content()) to position your text.
    6. Read the info for the API calls to make sure you understand the requirements and arguments
    7. When you make a selection, clear it once you no longer need it

    Here are some general tips for when working with Photoshop.

    In general, layers are created from bottom up, so keep that in mind as you figure out the order or operations. If you want you have lower layers show through higher ones you must either change the opacity of the higher layers and / or blend modes.

    When using fonts there are a couple of things to keep in mind. First, the font origin is the bottom left of the font, not the top right.

    Suggestions for sizes:
    Paragraph text : 8 to 12 pts
    Headings : 14 - 20 pts
    Single Word Large : 20 to 25pt

    Pay attention to what layer names are needed for. Sometimes the specify the name of a newly created layer and sometimes they specify the name of the layer that the action should be performed on.

    As a general rule, you should not flatten files unless asked to do so, or its necessary to apply an effect or look.

    When generating an image, you do not need to first create a pixel layer. A layer will automatically be created when you generate the image.

    Colors are defined via a dict with red, green and blue properties with values between 0 and 255
    {{"red":255, "green":0, "blue":0}}

    Bounds is defined as a dict with top, left, bottom and right properties
    {{"top": 0, "left": 0, "bottom": 250, "right": 300}}

    Valid options for API calls:

    alignment_modes: {", ".join(alignment_modes)}

    justification_modes: {", ".join(justification_modes)}

    blend_modes: {", ".join(blend_modes)}

    anchor_positions: {", ".join(anchor_positions)}

    interpolation_methods: {", ".join(interpolation_methods)}

    warp_styles: {", ".join(warp_styles)}

    bevel_emboss_styles: {", ".join(bevel_emboss_styles)}

    bevel_emboss_techniques: {", ".join(bevel_emboss_techniques)}

    gradient_types: {", ".join(gradient_types)}

    smart_sharpen_remove_types: {", ".join(smart_sharpen_remove_types)}

    radial_blur_methods: {", ".join(radial_blur_methods)}

    radial_blur_qualities: {", ".join(radial_blur_qualities)}

    zigzag_styles: {", ".join(zigzag_styles)}

    wave_types: {", ".join(wave_types)}

    spherize_modes: {", ".join(spherize_modes)}

    selective_color_targets: {", ".join(selective_color_targets)}

    trim_types: {", ".join(trim_types)}

    stroke_positions: {", ".join(stroke_positions)}

    glow_sources: {", ".join(glow_sources)}

    curves_channels: {", ".join(curves_channels)}

    noise_distributions: {", ".join(noise_distributions)}

    fonts: {", ".join(font_names[:FONT_LIMIT])}
    """

font_names = list_all_fonts_postscript()

interpolation_methods = [
   "AUTOMATIC",
   "BICUBIC",
   "BICUBICSHARPER",
   "BICUBICSMOOTHER",
   "BILINEAR",
   "NEARESTNEIGHBOR"
]

anchor_positions = [
   "BOTTOMCENTER",
   "BOTTOMLEFT", 
   "BOTTOMRIGHT", 
   "MIDDLECENTER", 
   "MIDDLELEFT", 
   "MIDDLERIGHT", 
   "TOPCENTER", 
   "TOPLEFT", 
   "TOPRIGHT"
]

justification_modes = [
    "CENTER",
    "CENTERJUSTIFIED",
    "FULLYJUSTIFIED",
    "LEFT",
    "LEFTJUSTIFIED",
    "RIGHT",
    "RIGHTJUSTIFIED"
]

alignment_modes = [
    "LEFT",
    "CENTER_HORIZONTAL",
    "RIGHT",
    "TOP",
    "CENTER_VERTICAL",
    "BOTTOM"
]

blend_modes = [
    "COLOR",
    "COLORBURN",
    "COLORDODGE",
    "DARKEN",
    "DARKERCOLOR",
    "DIFFERENCE",
    "DISSOLVE",
    "DIVIDE",
    "EXCLUSION",
    "HARDLIGHT",
    "HARDMIX",
    "HUE",
    "LIGHTEN",
    "LIGHTERCOLOR",
    "LINEARBURN",
    "LINEARDODGE",
    "LINEARLIGHT",
    "LUMINOSITY",
    "MULTIPLY",
    "NORMAL",
    "OVERLAY",
    "PASSTHROUGH",
    "PINLIGHT",
    "SATURATION",
    "SCREEN",
    "SOFTLIGHT",
    "SUBTRACT",
    "VIVIDLIGHT"
]

warp_styles = [
    "arc", "arcLower", "arcUpper", "arch", "bulge",
    "shellLower", "shellUpper", "flag", "wave", "fish",
    "rise", "fisheye", "inflate", "squeeze", "twist"
]

bevel_emboss_styles = [
    "outerBevel", "innerBevel", "emboss", "pillowEmboss", "strokeEmboss"
]

bevel_emboss_techniques = [
    "smooth", "chiselHard", "chiselSoft"
]

gradient_types = [
    "linear", "radial", "angle", "reflected", "diamond"
]

smart_sharpen_remove_types = [
    "gaussianBlur", "lensBlur", "motionBlur"
]

radial_blur_methods = [
    "spin", "zoom"
]

radial_blur_qualities = [
    "draft", "good", "best"
]

zigzag_styles = [
    "aroundCenter", "outFromCenter", "pondRipples"
]

wave_types = [
    "sine", "triangle", "square"
]

spherize_modes = [
    "normal", "horizontal", "vertical"
]

selective_color_targets = [
    "reds", "yellows", "greens", "cyans", "blues", "magentas", "whites", "neutrals", "blacks"
]

trim_types = [
    "transparent", "topLeftPixelColor", "bottomRightPixelColor"
]

stroke_positions = [
    "CENTER", "INSIDE", "OUTSIDE"
]

glow_sources = [
    "edge", "center"
]

curves_channels = [
    "composite", "red", "green", "blue"
]

noise_distributions = [
    "uniform", "gaussian"
]


# =============================================================================
# HELPER: select a layer by ID via batchPlay (no UXP command handler needed)
# =============================================================================

def _select_layer_bp(layer_id: int):
    """Internal helper — selects a layer by ID using batchPlay."""
    commands = [{
        "_obj": "select",
        "_target": [{"_ref": "layer", "_id": layer_id}],
        "makeVisible": False,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# EXECUTE BATCHPLAY — THE "GOD TOOL"
# =============================================================================

@mcp.tool()
def execute_batchplay(commands: list) -> dict:
    """
    Execute arbitrary Photoshop batchPlay commands. This is the most powerful tool —
    it can do ANYTHING Photoshop can do by sending raw batchPlay descriptors directly.

    Use this when no specific tool exists for what you need (e.g., Plastic Wrap filter,
    Glass distortion, Chrome effect, custom blend-if, advanced layer operations, etc.).

    Args:
        commands: A list of batchPlay descriptor dicts. Each dict represents one Photoshop
                  action. Example: [{"_obj": "gaussianBlur", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}], "radius": {"_unit": "pixelsUnit", "_value": 5.0}}]

    Returns:
        dict: The result from Photoshop after executing the command(s).
    """
    if not commands:
        raise ValueError("commands list cannot be empty")

    command = createCommand(
        "executeBatchPlayCommand",
        {"commands": commands}
    )
    return sendCommand(command)


# =============================================================================
# PLASTIC WRAP FILTER (via batchPlay)
# =============================================================================

@mcp.tool()
def apply_plastic_wrap(layer_id: int, highlight_strength: int = 15, detail: int = 9, smoothness: int = 7) -> dict:
    """
    Applies Plastic Wrap filter to a layer for a liquid/chrome/wet look.

    Args:
        layer_id: ID of the layer to apply the effect to
        highlight_strength: Strength of highlights (0-20). Default 15.
        detail: Detail level (1-15). Default 9.
        smoothness: Smoothness (1-15). Default 7.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "plasticWrap",
        "highlightStrength": highlight_strength,
        "detail": detail,
        "smoothness": smoothness,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# GLASS DISTORTION FILTER
# =============================================================================

@mcp.tool()
def apply_glass_distortion(layer_id: int, distortion: int = 5, smoothness: int = 3, texture: str = "frosted", scaling: int = 100) -> dict:
    """
    Applies Glass distortion filter for liquid/glass refraction look.

    Args:
        layer_id: ID of the layer
        distortion: Distortion amount (0-20). Default 5.
        smoothness: Smoothness (1-15). Default 3.
        texture: Texture type — 'frosted', 'blocks', 'canvas', 'tinyLens'. Default 'frosted'.
        scaling: Texture scale percentage (50-200). Default 100.
    """
    _select_layer_bp(layer_id)

    texture_map = {
        "frosted": 1,
        "blocks": 2,
        "canvas": 3,
        "tinyLens": 4,
    }
    texture_id = texture_map.get(texture, 1)

    commands = [{
        "_obj": "glass",
        "distortion": distortion,
        "smoothness": smoothness,
        "textureType": texture_id,
        "scaling": scaling,
        "invert": False,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# RIPPLE DISTORTION FILTER
# =============================================================================

@mcp.tool()
def apply_ripple(layer_id: int, amount: int = 100, size: str = "medium") -> dict:
    """
    Applies Ripple distortion filter.

    Args:
        layer_id: ID of the layer
        amount: Ripple amount (-999 to 999). Default 100.
        size: Ripple size — 'small', 'medium', 'large'. Default 'medium'.
    """
    _select_layer_bp(layer_id)

    size_map = {"small": 0, "medium": 1, "large": 2}
    size_val = size_map.get(size, 1)

    commands = [{
        "_obj": "ripple",
        "amount": amount,
        "rippleSize": size_val,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# OCEAN RIPPLE DISTORTION FILTER
# =============================================================================

@mcp.tool()
def apply_ocean_ripple(layer_id: int, ripple_size: int = 9, ripple_magnitude: int = 9) -> dict:
    """
    Applies Ocean Ripple distortion filter for water surface effect.

    Args:
        layer_id: ID of the layer
        ripple_size: Size of ripples (1-15). Default 9.
        ripple_magnitude: Magnitude of ripples (1-20). Default 9.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "oceanRipple",
        "rippleSize": ripple_size,
        "rippleMagnitude": ripple_magnitude,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# CHROME FILTER (via batchPlay)
# =============================================================================

@mcp.tool()
def apply_chrome_filter(layer_id: int, detail: int = 4, smoothness: int = 7) -> dict:
    """
    Applies Chrome filter for metallic/liquid chrome look.

    Args:
        layer_id: ID of the layer
        detail: Detail level (0-10). Default 4.
        smoothness: Smoothness (0-10). Default 7.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "chrome",
        "detail": detail,
        "smoothness": smoothness,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# SET BLEND-IF SLIDERS
# =============================================================================

@mcp.tool()
def set_layer_blend_if(layer_id: int,
                       this_layer_black: int = 0,
                       this_layer_black_feather: int = 0,
                       this_layer_white: int = 255,
                       this_layer_white_feather: int = 255,
                       underlying_black: int = 0,
                       underlying_black_feather: int = 0,
                       underlying_white: int = 255,
                       underlying_white_feather: int = 255) -> dict:
    """
    Sets the Blend If sliders for a layer (Layer Style > Blending Options).
    Controls which tonal ranges are visible/hidden for seamless compositing.

    Split points: black_feather > black, white_feather < white for smooth transitions.

    Args:
        layer_id: ID of the layer
        this_layer_black: This Layer dark cutoff (0-255). Default 0.
        this_layer_black_feather: This Layer dark feather point (0-255). Default 0.
        this_layer_white: This Layer light cutoff (0-255). Default 255.
        this_layer_white_feather: This Layer light feather point (0-255). Default 255.
        underlying_black: Underlying Layer dark cutoff (0-255). Default 0.
        underlying_black_feather: Underlying Layer dark feather point (0-255). Default 0.
        underlying_white: Underlying Layer light cutoff (0-255). Default 255.
        underlying_white_feather: Underlying Layer light feather point (0-255). Default 255.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "set",
        "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}],
        "to": {
            "_obj": "layer",
            "blendRange": [{
                "_obj": "blendRange",
                "channel": {"_ref": "channel", "_enum": "channel", "_value": "gray"},
                "srcBlackMin": this_layer_black,
                "srcBlackMax": this_layer_black_feather,
                "srcWhiteMin": this_layer_white_feather,
                "srcWhiteMax": this_layer_white,
                "destBlackMin": underlying_black,
                "destBlackMax": underlying_black_feather,
                "destWhiteMin": underlying_white_feather,
                "destWhiteMax": underlying_white,
            }]
        },
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# MERGE SPECIFIC LAYERS
# =============================================================================

@mcp.tool()
def merge_layers(layer_ids: list) -> dict:
    """
    Merges specific layers into one. Selects the given layers and merges them.

    Args:
        layer_ids: List of layer IDs to merge together.
    """
    if not layer_ids or len(layer_ids) < 2:
        raise ValueError("Need at least 2 layer IDs to merge")

    # Select first layer via batchPlay
    _select_layer_bp(layer_ids[0])

    # Add remaining layers to selection
    for lid in layer_ids[1:]:
        commands = [{
            "_obj": "select",
            "_target": [{"_ref": "layer", "_id": lid}],
            "selectionModifier": {"_enum": "selectionModifierType", "_value": "addToSelection"},
            "makeVisible": False,
            "_isCommand": True
        }]
        command = createCommand("executeBatchPlayCommand", {"commands": commands})
        sendCommand(command)

    # Merge selected layers
    commands = [{
        "_obj": "mergeLayersNew",
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# SELECT LAYER (utility — make a layer active without doing anything else)
# =============================================================================

@mcp.tool()
def select_layer(layer_id: int) -> dict:
    """
    Makes the specified layer the active/selected layer.

    Args:
        layer_id: ID of the layer to select/activate.
    """
    return _select_layer_bp(layer_id)


# =============================================================================
# APPLY FILTER TO LAYER MASK
# =============================================================================

@mcp.tool()
def select_layer_mask(layer_id: int) -> dict:
    """
    Selects (targets) the layer mask of the specified layer so that subsequent
    operations (paint, fill, filter) apply to the mask instead of the layer pixels.

    Args:
        layer_id: ID of the layer whose mask to select.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "select",
        "_target": [{"_ref": "channel", "_enum": "channel", "_value": "mask"}],
        "makeVisible": False,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


@mcp.tool()
def select_layer_rgb(layer_id: int) -> dict:
    """
    Selects the RGB composite channel of the specified layer (switches back from mask editing
    to normal pixel editing).

    Args:
        layer_id: ID of the layer.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "select",
        "_target": [{"_ref": "channel", "_enum": "channel", "_value": "RGB"}],
        "makeVisible": False,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# ADD LAYER MASK (White = reveal all, Black = hide all)
# =============================================================================

@mcp.tool()
def add_layer_mask_reveal_all(layer_id: int) -> dict:
    """
    Adds a white (reveal all) layer mask to the specified layer.

    Args:
        layer_id: ID of the layer to add mask to.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "make",
        "new": {"_class": "channel"},
        "at": {"_ref": "channel", "_enum": "channel", "_value": "mask"},
        "using": {"_enum": "userMaskEnabled", "_value": "revealAll"},
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


@mcp.tool()
def add_layer_mask_hide_all(layer_id: int) -> dict:
    """
    Adds a black (hide all) layer mask to the specified layer.

    Args:
        layer_id: ID of the layer to add mask to.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "make",
        "new": {"_class": "channel"},
        "at": {"_ref": "channel", "_enum": "channel", "_value": "mask"},
        "using": {"_enum": "userMaskEnabled", "_value": "hideAll"},
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# FILL LAYER MASK WITH GRADIENT (for smooth fade effects)
# =============================================================================

@mcp.tool()
def fill_mask_with_gradient(layer_id: int, start_x: int = 0, start_y: int = 0, end_x: int = 0, end_y: int = 100, gradient_type: str = "linear") -> dict:
    """
    Fills the layer mask with a black-to-white gradient (for smooth fade/transition effects).
    The layer must already have a mask.

    Args:
        layer_id: ID of the layer with a mask.
        start_x: Gradient start X. Default 0.
        start_y: Gradient start Y. Default 0.
        end_x: Gradient end X. Default 0.
        end_y: Gradient end Y. Default 100.
        gradient_type: 'linear', 'radial', 'angle', 'reflected', 'diamond'. Default 'linear'.
    """
    # Select the layer then its mask
    _select_layer_bp(layer_id)

    mask_cmd = createCommand("executeBatchPlayCommand", {"commands": [{
        "_obj": "select",
        "_target": [{"_ref": "channel", "_enum": "channel", "_value": "mask"}],
        "makeVisible": False,
        "_isCommand": True
    }]})
    sendCommand(mask_cmd)

    type_map = {
        "linear": "linear",
        "radial": "radial",
        "angle": "angular",
        "reflected": "reflected",
        "diamond": "diamond"
    }
    grad_type = type_map.get(gradient_type, "linear")

    # Draw gradient on mask
    commands = [{
        "_obj": "gradientClassEvent",
        "from": {"_obj": "paint", "horizontal": start_x, "vertical": start_y},
        "to": {"_obj": "paint", "horizontal": end_x, "vertical": end_y},
        "type": {"_enum": "gradientType", "_value": grad_type},
        "gradient": {
            "_obj": "gradientClassEvent",
            "name": "Foreground to Background",
            "gradientForm": {"_enum": "gradientForm", "_value": "customStops"},
            "interfaceIconFrameDimmed": 4096,
            "colors": [
                {
                    "_obj": "colorStop",
                    "color": {"_obj": "grayscale", "gray": 0},
                    "type": {"_enum": "colorStopType", "_value": "userStop"},
                    "location": 0, "midpoint": 50
                },
                {
                    "_obj": "colorStop",
                    "color": {"_obj": "grayscale", "gray": 100},
                    "type": {"_enum": "colorStopType", "_value": "userStop"},
                    "location": 4096, "midpoint": 50
                }
            ],
            "transparency": [
                {"_obj": "transferSpec", "opacity": {"_unit": "percentUnit", "_value": 100}, "location": 0, "midpoint": 50},
                {"_obj": "transferSpec", "opacity": {"_unit": "percentUnit", "_value": 100}, "location": 4096, "midpoint": 50}
            ]
        },
        "opacity": {"_unit": "percentUnit", "_value": 100},
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    result = sendCommand(command)

    # Switch back to RGB
    rgb_cmd = createCommand("executeBatchPlayCommand", {"commands": [{
        "_obj": "select",
        "_target": [{"_ref": "channel", "_enum": "channel", "_value": "RGB"}],
        "makeVisible": False,
        "_isCommand": True
    }]})
    sendCommand(rgb_cmd)

    return result


# =============================================================================
# POLAR COORDINATES FILTER
# =============================================================================

@mcp.tool()
def apply_polar_coordinates(layer_id: int, conversion: str = "rectangularToPolar") -> dict:
    """
    Applies Polar Coordinates distortion filter.

    Args:
        layer_id: ID of the layer
        conversion: 'rectangularToPolar' or 'polarToRectangular'. Default 'rectangularToPolar'.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "polarCoordinates",
        "conversion": {"_enum": "polarConversionType", "_value": conversion},
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# SHEAR FILTER
# =============================================================================

@mcp.tool()
def apply_shear(layer_id: int, points: list = None, undefined_area: str = "wrapAround") -> dict:
    """
    Applies Shear distortion filter along a curve defined by control points.

    Args:
        layer_id: ID of the layer
        points: List of {x, y} dicts defining the shear curve (0-255 range). Default straight line.
        undefined_area: 'wrapAround' or 'repeatEdgePixels'. Default 'wrapAround'.
    """
    if points is None:
        points = [{"x": 0, "y": 0}, {"x": 255, "y": 255}]

    _select_layer_bp(layer_id)

    curve_points = [{"_obj": "paint", "horizontal": p["x"], "vertical": p["y"]} for p in points]

    commands = [{
        "_obj": "shear",
        "shearPoints": curve_points,
        "undefinedArea": {"_enum": "undefinedArea", "_value": undefined_area},
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


# =============================================================================
# PINCH DISTORTION FILTER
# =============================================================================

@mcp.tool()
def apply_pinch(layer_id: int, amount: int = 50) -> dict:
    """
    Applies Pinch distortion filter (inward/outward squeeze).

    Args:
        layer_id: ID of the layer
        amount: Pinch amount (-100 to 100). Positive = inward, negative = outward. Default 50.
    """
    _select_layer_bp(layer_id)

    commands = [{
        "_obj": "pinch",
        "amount": amount,
        "_isCommand": True
    }]
    command = createCommand("executeBatchPlayCommand", {"commands": commands})
    return sendCommand(command)


if __name__ == "__main__":
    mcp.run()
