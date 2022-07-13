import numpy as np

def compare_projections(point, camera_mtx, opengl_mtx, w, h):
    # print(point)
    #     
    # screen_point, _ = cv2.projectPoints(np.array([point]), np.zeros(3), np.zeros(3), camera_mtx, np.zeros(5))
    # print(screen_point)

    #Note: we obtain the same result with this: (that's what cv2.projectPoints basically does: multiply points with camera matrix and then divide result by z coord)
    open_cv = camera_mtx.dot(point)/point[2]
    # print(open_cv)


    #### OpenGL projection
    #we flip the point z coord, because in opengl camera is oriented along -Oz axis
    point[2] = -point[2]
    point2 = np.hstack([point,1.0]) #we add vertex w coord (usually done in vertex shader before multiplying by projection matrix)
    #we get the point in clip space

    clip_point = opengl_mtx.dot(point2)

    #NOTE: what follows "simulates" what happens in OpenGL after the vertex shader.
    #This is necessary so that we can make sure our projection matrix will yield the correct result when used in OpenGL
    #we get the point in NDC

    ndc_point = clip_point / clip_point[3]
    #we get the screen coordinates
    viewport_point = (ndc_point + 1.0)/2.0 * np.array([w, h, 1.0, 1.0])
    #opencv Oy convention is opposite of OpenGL so we reverse y coord
    viewport_point[1] = h - viewport_point[1]
    
    # print(viewport_point)
    # print()

def project_opencv(points, camera_mtx):
    projection = []

    for point in points:
        open_cv = camera_mtx.dot(point)/point[2]
        projection.append([open_cv[0], open_cv[1]])

    return projection
   
def project_opengl(points, opengl_mtx, w, h):
    projection = []

    for point in points:
        #### OpenGL projection
        #we flip the point z coord, because in opengl camera is oriented along -Oz axis
        point[2] = -point[2]
        point2 = np.hstack([point,1.0]) #we add vertex w coord (usually done in vertex shader before multiplying by projection matrix)
        #we get the point in clip space
        clip_point = opengl_mtx.dot(point2)
        # print('point= ', point2)
        # print('dot= ',  np.dot(opengl_mtx, point2))
      

        # print('point = ', point2)
        # print('clip_point= ',clip_point)

        #NOTE: what follows "simulates" what happens in OpenGL after the vertex shader.
        #This is necessary so that we can make sure our projection matrix will yield the correct result when used in OpenGL
        #we get the point in NDC

        ndc_point = clip_point / clip_point[3]
        # print('ndc_point= ',ndc_point,'    ' )
        
        x = (ndc_point * np.array([w, h, 1.0, 1.0]))
        # print('x= ',ndc_point)

        

        #we get the screen coordinates
        viewport_point = (ndc_point + 1.0)/2.0 * np.array([w, h, 1.0, 1.0])
        # print('viewport_point= ',viewport_point, '\n')
        
        #opencv Oy convention is opposite of OpenGL so we reverse y coord
        viewport_point[1] = h - viewport_point[1]
        # print('viewport_point= ',viewport_point, '\n')
        
        # print(viewport_point)
        projection.append([viewport_point[0], viewport_point[1]])
        
    return projection