from mpu6050 import mpu6050


# todo singleton class? error handling if created twice?

class IMU:
    def __init__(self):
        self.sensor = mpu6050(0x68)

    def get_accel_data(self):
        return self.sensor.get_accel_data()

    def get_temp(self):
        return self.sensor.get_temp()

    def get_gyro_data(self):
        return self.sensor.get_gyro_data()


if __name__ == "__main__":
    mpu = mpu6050(0x68)
    print(mpu.get_temp())
    accel_data = mpu.get_accel_data()
    print(accel_data['x'])
    print(accel_data['y'])
    print(accel_data['z'])
    gyro_data = mpu.get_gyro_data()
    print(gyro_data['x'])
    print(gyro_data['y'])
    print(gyro_data['z'])
