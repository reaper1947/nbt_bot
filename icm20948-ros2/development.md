# ICM20948 on the RPi

Started with Ubuntu 22.04LTS image for the RPi.

Installed the Pimoroni Python library.

```bash
sudo pip3 install icm20948
```

Connected the IMU as follows:

| ICM20948 Pin | BCM Pin | Actual Pin |
|:----:|:-:|:-:|
| 2-5V | - | 1 |
| SDA  | 2 | 3 |
| SCL  | 3 | 5 |
| GND  | - | 6 |

Installed the I2C tools package and see if it can detect the IMU.

```bash
sudo apt install i2c-tools
sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Great.  Now add user to `dialout` group.

```bash
sudo adduser $USER dialout
```

Log out and in again and tried the command `i2cdetect -y 1`.  Worked so this is all set up.

Downloaded the Pimoroni ICM20948 repo:

```bash
cd ~/git
git clone https://github.com/pimoroni/icm20948-python.git
cd icm20948-python/examples
python3 read-all.py
```

This worked and the numbers changed when the IMU was moved.

## Building the driver

I based the driver on some old code that I wrote for another IMU.  Most of the code high level code was copied into this repo, renamed as needed, built and tested.  Once that was done, the code in the file `imu.py` was modified to use the Pimoroni ICM20948 library.

Time was short when developing this driver, so I have no idea if the digital motion processor (DMP) on the ICM20948 is being used or not.  If performance is an issue, I will need to implement my own driver but for now this will have to do.
