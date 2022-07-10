# PyBlock3D
Minecraft budget ripoff
<br />
# Goals <br/>
 - [x] Render a simple 3d plane using pygame
 - [x] Render simple objects
 - [x] Add a player for the user to use
 - [x] Optimize memory usage
 - [ ] Optimize Rendering
 - [ ] Add player mechanics
 - [ ] Create a world for the player to interact with
 - [ ] Implement a UI

# Completed Goals - Break Down
Render simple 3D plane / point: <br/>
Utilizing projection techniques, we were able to project 3D points or objects, maping them onto a 2D plane, which would represent the user's display. We specifically utilized prespective projection, as it suited the game the most (since it is a first person game).<br/><br/>
We implemented the projection of any 3D point under the renderer.py script, which provides the renderer class. Using the script, a renderer object can be created. To render 3d points using this object, the render function is called, it too calling upon the two other functions in the renderer class (posToCam; returns 3D vector of the points distance from the camera, and posOnDisp; returns 2D vector of the points projection on the display).<br/><br/>
The posToCam function finds the difference between the x, y, z coordinates of 3D point A, and the Camera (To be continued) </p><br/>
Optimize memory usage: <br/>
To limit amount of information in memory, and the amount of blocks required to be rendered on the screen. The application doesn't render any blocks outside of a certain radius to the user. These unloaded blocks are also ofloaded from the memory into a file.
