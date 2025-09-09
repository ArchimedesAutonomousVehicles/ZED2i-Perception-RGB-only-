import cv2, yaml, argparse, numpy as np
p = argparse.ArgumentParser()
p.add_argument("--left", required=True); p.add_argument("--right", required=True); p.add_argument("--calib", required=True)
args = p.parse_args()

with open(args.calib) as f: C = yaml.safe_load(f)
K1 = np.array(C["K_left"]);  D1 = np.array(C["D_left"]).ravel()
K2 = np.array(C["K_right"]); D2 = np.array(C["D_right"]).ravel()
R  = np.array(C["R"]);       T  = np.array(C["T"]).ravel()

L = cv2.imread(args.left,  cv2.IMREAD_GRAYSCALE)
Rimg = cv2.imread(args.right, cv2.IMREAD_GRAYSCALE)
h,w = L.shape[:2]
R1,R2,P1,P2,Q,_,_ = cv2.stereoRectify(K1,D1,K2,D2,(w,h),R,T,alpha=0)
m1x,m1y = cv2.initUndistortRectifyMap(K1,D1,R1,P1,(w,h),cv2.CV_32FC1)
m2x,m2y = cv2.initUndistortRectifyMap(K2,D2,R2,P2,(w,h),cv2.CV_32FC1)
Lr = cv2.remap(L,m1x,m1y,cv2.INTER_LINEAR); Rr = cv2.remap(Rimg,m2x,m2y,cv2.INTER_LINEAR)

sgbm = cv2.StereoSGBM_create(minDisparity=0,numDisparities=64,blockSize=5,P1=8*3*25,P2=32*3*25,mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
disp = sgbm.compute(Lr,Rr).astype(np.float32)/16.0
disp_viz = cv2.normalize(disp,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
cv2.imwrite("results/disparity.png", disp_viz)
print("Saved results/disparity.png")
