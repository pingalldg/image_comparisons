from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
def compare_images(imageA, imageB, title,str,ms,sim):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    # setup the figure
    fig = plt.figure(title)
    fig = plt.figure(figsize=(6.4, 4.8), dpi=1000)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
    ms.append(m)
    sim.append(s)
    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")
    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")
    # show the images
    plt.savefig(str)
    fig.clear()
    fig.clf()
# load the images -- the original, the hydro + ampt,
# and the hydro+ampt
ms2=[]
sim2=[]
tau=[0.2,0.6,0.8,1.0,1.2,1.6,2.0,3.0,4.0,5.0]
for i in range(10):    
    str1="images_4guass_etas0_temp_etabys16/tau"+str(i)+".png"
    str2="ampt_4guass_etas0_temp/tau"+str(i)+".png"
    hydro= cv2.imread(str1,cv2.IMREAD_UNCHANGED)
    ampt = cv2.imread(str2,cv2.IMREAD_UNCHANGED)
    # convert the images to grayscale
    hydro = cv2.cvtColor(hydro, cv2.COLOR_BGR2GRAY)
    ampt = cv2.cvtColor(ampt, cv2.COLOR_BGR2GRAY)
    # initialize the figure
    fig = plt.figure("Images")
    images = ("Hydro", hydro), ("AMPT", ampt)
    str3="similairity_etas0_04guass_TbyTMax_etabys16/SSIM/gray_image"+str(i)+".pdf"
    compare_images(hydro,ampt, "Hydro vs. AMPT",str3,ms2,sim2)
    
plt.clf()    
    
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(tau,ms2,".",label=r"$\sigma_{smear}=0.4$")
ax.set_xlabel(r"$\tau$( fm)")
ax.set_ylabel("MSE")
plt.legend(fontsize=14)
plt.savefig("ms_vs_tau_TbyTmax_etabys16.pdf")
plt.clf()
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(tau,sim2,".",label=r"$\sigma_{smear}=0.4$")
ax.set_xlabel(r"$\tau$( fm)")
ax.set_ylabel("Similarity Index")
plt.legend(fontsize=14)


file1=open("myfile_etabys16_TbyTmax.dat", "w")  
for i in range(len(tau)):
    print(tau[i],ms2[i],sim2[i],file=file1)
plt.savefig("sim_vs_tau_TbyTmax_etabys16.pdf")
