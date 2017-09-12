
import pylab as plt
import numpy as np
import sys
import chardet

def main(argv):
    f= open(argv[1])
    f_read=f.read()
    f_charInfo=chardet.detect(f_read)
    print(f_charInfo)
	
    f_read_decode=f_read.decode(f_charInfo['encoding'])

    lines = f_read_decode.readlines()
	
    bitrate = []
    jitter = []
    loss_ratio = []
    fps = []
    for line in lines:
        if line.find("recv stats")!=-1:
            tmp_splite = line.split()
            for i in range(len(tmp_splite)):
                if tmp_splite[i]=='jitter':
                    jitter.append(int(tmp_splite[i+1])/90)
                elif tmp_splite[i]=='ratio':
                    loss_ratio.append(int(tmp_splite[i+1]))
                elif tmp_splite[i]=='bitrate':
                    bitrate.append(int(tmp_splite[i+1])/1000.0)
                elif tmp_splite[i]=='fps':
                    fps.append(int(tmp_splite[i+1]))
                
    bitrate_average = np.convolve( bitrate, np.ones( (10,), dtype="float" ),mode="valid") /10.
    
    plt.plot(jitter,label="jitter(ms)")
    plt.plot(bitrate_average,label="bitrate(kbps)")
    plt.plot(loss_ratio,label="loss ratio(%)")
    plt.xlabel("time(sec)")
    plt.legend()
    plt.title("log analysis")
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
