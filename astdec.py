import asyenc
file_content = b"""JointCloud is a cross-cloud cooperation architecture for integrated Internet service customization. The customized cross-cloud storage service based on this architecture is called JointCloud storage. Storing the Internet of Things (IoT) big data in erasure-coded JointCloud storage systems ensures that data can be accessed when several cloud services interrupt. However, because existing erasure codes cannot adapt the generator matrix and data placement scheme to different network environments and encoding parameters, they usually incur a large network resource consumption (NRC) for repairing data in JointCloud storage systems. """
obj = asyenc.Asyencryption()
enc,key = obj.encryption(file_content)
print("Encryption Content : "+ enc)
print("Public Key : "+ key)

