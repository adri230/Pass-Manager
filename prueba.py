from fido2.hid import CtapHidDevice

def detect_fido2_key():
    devices = list(CtapHidDevice.list_devices())
    if devices:
        print("Llave FIDO2 conectada:")
    else:
        print("No hay ninguna llave FIDO2 conectada.")

if __name__ == "__main__":
    detect_fido2_key()