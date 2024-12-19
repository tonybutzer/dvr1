- tv) tony@dopey:~/opt/dvr1$ mkdir 1_livetv
- (tv) tony@dopey:~/opt/dvr1$ mkdir 2_tuner_daemon
- (tv) tony@dopey:~/opt/dvr1$ mkdir 3_diagnostic_tools
- (tv) tony@dopey:~/opt/dvr1$ mkdir libdvr


# dvr1
new inproved hd dvr


## Preparing the Linux box

### installing mint 22

1. download the iso
2. sudo dd if=/path/to/your/iso/image.iso of=/dev/sdb bs=4M conv=sync,noerror


# Ventoy

Here's how to add an ISO to Ventoy:

**Prerequisites:**

* **Ventoy Installed USB Drive:** You'll need a USB drive with Ventoy installed. If not, follow the instructions on the Ventoy website to create one.
* **ISO Image:** The ISO file of the operating system or software you want to boot.

**Steps:**

1. **Connect the Ventoy Drive:** Plug your Ventoy USB drive into your computer.
2. **Open the Ventoy Partition:** Locate the Ventoy partition on your computer. It will usually be labeled as "Ventoy" or something similar.
3. **Copy the ISO:** Simply copy the ISO file to the Ventoy partition. You can drag and drop or use the copy-paste method.

**That's it!** Ventoy will automatically detect the ISO and add it to the boot menu.

**How to Boot:**

1. **Restart Your Computer:** Restart your computer with the Ventoy drive plugged in.
2. **Select the ISO:** During the boot process, you should see a boot menu. Use the arrow keys to select the desired ISO and press Enter.

**Additional Tips:**

* **Multiple ISOs:** You can add multiple ISOs to the Ventoy drive. Ventoy will display them in the boot menu.
* **File System:** Ventoy supports various file systems, including FAT32, exFAT, NTFS, and EXT4.
* **Secure Boot:** If you're using a system with Secure Boot enabled, you might need to disable it temporarily to boot from Ventoy.

**For more detailed instructions and troubleshooting, refer to the official Ventoy documentation:** [https://www.ventoy.net/en/doc_start.html](https://www.ventoy.net/en/doc_start.html)


