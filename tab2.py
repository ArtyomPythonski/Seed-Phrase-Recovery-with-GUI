from tkinter import *
import tkinter as tk
from hdwallet import BIP44HDWallet
from hdwallet.symbols import ETH
from list import seeds
from itertools import permutations
import threading

def create_tab2(notebook):
    tab2 = tk.Frame(notebook)
    background_color = "#F1F6F5"
    tab2.config(bg=background_color)

    # Create widgets for tab 2
    def pop_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    def copy():
        t.event_generate("<<Copy>>")

    def delete():
        words.delete(0, END)
        start_address_entry.delete(0, END)
        end_address_entry.delete(0, END)
        whole_address_entry.delete(0, END)
        mixed_words_entry.delete(0, END)

    def stop():
        global running
        running = False


    # Instruction Frame
    instruction_frame = tk.Frame(tab2, width=70, height=50, bg="#F2F2F2", highlightthickness=2, pady=20, padx=20, highlightbackground="#0081C9", highlightcolor="#0081C9")
    instruction_frame.grid(row=0, column=0, pady=20, padx=20)
    # Output Frame
    text_output_frame = tk.Frame(tab2, bg=background_color, highlightthickness=0, padx=20)
    text_output_frame.grid(row=3, column=0, pady=5)

    # Instructions
    main_description = tk.Label(instruction_frame,bg="#F2F2F2",fg="#0081C9",text='Enter the seed phrase marking with "???" the position of unknown words, and enter mixed words that you familiar with', font=("Arial", 10) )
    main_description.grid(row=0, column=1)
    #=======================================================================================================
    # Description Label - Seed Phrase 
    seed_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Seed Phrase Pattern: ")
    seed_label.grid(row=1, column=0)
    # Input of unknown words
    words = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=1)
    words.grid(row=1, column=1)
    #=======================================================================================================
    # Description Label - Mix Words
    mixed_words_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Mixed Words: ")
    mixed_words_label.grid(row=2, column=0)
    # Mix address input
    mixed_words_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    mixed_words_entry.grid(row=2, column=1)
    # Description Label - Start Address
    start_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Start of Address: ")
    start_address_label.grid(row=3, column=0)
    # Start of Address Input
    start_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    start_address_entry.grid(row=3, column=1)
    #=======================================================================================================
    # Description Label - End Address
    end_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="End of Address: ")
    end_address_label.grid(row=4, column=0)
    # End of Address Input
    end_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    end_address_entry.grid(row=4, column=1)
    #=======================================================================================================
    # Description Label - Whole Address
    whole_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Whole Address: ")
    whole_address_label.grid(row=5, column=0)
    # Input of Whole Address
    whole_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    whole_address_entry.grid(row=5, column=1)
    #=======================================================================================================
    # Checkbox for enabling/disabling whole address input, or partial address input
    def Checked():
        
        if var.get() == 1:
            whole_address_entry.config(state=NORMAL)
            start_address_entry.config(state=DISABLED)
            end_address_entry.config(state=DISABLED)
        elif var.get() == 0:
            whole_address_entry.config(state=DISABLED)
            start_address_entry.config(state=NORMAL)
            end_address_entry.config(state=NORMAL)

    var = IntVar()
    checkbox_address = tk.Checkbutton(instruction_frame, bg="#F2F2F2", fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", highlightthickness=0, text="Whole Address\Partial Address", variable=var, command=Checked, onvalue=1, offvalue=0, border=None)
    checkbox_address.deselect()
    checkbox_address.invoke()
    checkbox_address.grid(row=6, column=1, sticky="W")

    # Descriptoin Label Text Output
    text_output_label = tk.Label(text_output_frame, bg=background_color, fg="#0081C9", text="Output:")
    text_output_label.grid(row=0, column=2)
    # Showing text output with the scroll function
    text_frame = tk.Frame(text_output_frame, background="yellow", width=100, height=90)
    text_frame.grid(row=1, column=2)
    scrollbar = tk.Scrollbar(text_frame)
    t = tk.Text(
        text_frame,
        bg="#F2F2F2",
        fg="#0081C9",
        highlightbackground="#0081C9",
        highlightcolor="#0081C9",
        height=10,
        width=100,
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=t.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    t.pack()

    # Right Click menu
    menu = tk.Menu(t, tearoff=0, bg="black", fg="white")
    # Options
    menu.add_command(label="Copy", command=copy)
    # Make the menu pop-up
    t.bind("<Button - 3>", pop_menu)

    # Buttons frame(copy)
    buttons_frame = tk.Frame(tab2, width=300, height=20, bg=background_color, highlightthickness=0, pady=5, padx=20)
    buttons_frame.grid(row=4, column=0)

    # Start Button
    def MyClick():

        global running
        running = True
        # getting words from Seed input and deleting additional spaces if present
        seed_phrase = (words.get().strip())

        # Getting addresses from Entry widget
        mixed_words = mixed_words_entry.get()
        beginning_of_the_address = start_address_entry.get()
        end_of_the_address = end_address_entry.get()
        whole_address = whole_address_entry.get()

        counter = 1
        comb = permutations(mixed_words.split())
        # 1 ???
        if seed_phrase.count("???") == 1:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                print(counter, seed1)
                #Insert result into text field
                t.insert(END, (f"{counter} {seed1}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed1)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed1}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed1}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 2 ???
        if seed_phrase.count("???") == 2:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                print(counter, seed2)
                #Insert result into text field
                t.insert(END, (f"{counter} {seed2}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed2)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed2}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed2}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 3 ???
        if seed_phrase.count("???") == 3:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                t.insert(END, (f"{counter} {seed3}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed3)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed3)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed3}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed3}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 4 ???
        if seed_phrase.count("???") == 4:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                t.insert(END, (f"{counter} {seed4}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed4)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed4)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed4}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed4}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 5 ???
        if seed_phrase.count("???") == 5:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                t.insert(END, (f"{counter} {seed5}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed5)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed5)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed5}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed5}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 6 ???
        if seed_phrase.count("???") == 6:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                t.insert(END, (f"{counter} {seed6}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed6)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed6)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed6}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed6}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 7 ???
        if seed_phrase.count("???") == 7:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                t.insert(END, (f"{counter} {seed7}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed7)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed7)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed7}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed7}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 8 ???
        if seed_phrase.count("???") == 8:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                seed8 = seed7.replace("???", str(x[7]), 1)
                t.insert(END, (f"{counter} {seed8}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed8)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed8)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed8}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed8}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 9 ???
        if seed_phrase.count("???") == 9:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                seed8 = seed7.replace("???", str(x[7]), 1)
                seed9 = seed8.replace("???", str(x[8]), 1)
                t.insert(END, (f"{counter} {seed9}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed9)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed9)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed9}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed9}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 10 ???
        if seed_phrase.count("???") == 10:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                seed8 = seed7.replace("???", str(x[7]), 1)
                seed9 = seed8.replace("???", str(x[8]), 1)
                seed10 = seed9.replace("???", str(x[9]), 1)
                t.insert(END, (f"{counter} {seed10}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed10)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed10)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed10}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed10}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 11 ???
        if seed_phrase.count("???") == 11:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                seed8 = seed7.replace("???", str(x[7]), 1)
                seed9 = seed8.replace("???", str(x[8]), 1)
                seed10 = seed9.replace("???", str(x[9]), 1)
                seed11 = seed10.replace("???", str(x[10]), 1)
                t.insert(END, (f"{counter} {seed11}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed11)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed11)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed11}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed11}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

        # 12 ???
        if seed_phrase.count("???") == 12:
            for x in comb:
                seed1 = seed_phrase.replace("???", str(x[0]), 1)
                seed2 = seed1.replace("???", str(x[1]), 1)
                seed3 = seed2.replace("???", str(x[2]), 1)
                seed4 = seed3.replace("???", str(x[3]), 1)
                seed5 = seed4.replace("???", str(x[4]), 1)
                seed6 = seed5.replace("???", str(x[5]), 1)
                seed7 = seed6.replace("???", str(x[6]), 1)
                seed8 = seed7.replace("???", str(x[7]), 1)
                seed9 = seed8.replace("???", str(x[8]), 1)
                seed10 = seed9.replace("???", str(x[9]), 1)
                seed11 = seed10.replace("???", str(x[10]), 1)
                seed12 = seed11.replace("???", str(x[11]), 1)
                t.insert(END, (f"{counter} {seed12}\n"))
                t.see(END)
                t.update()
                scrollbar.update()
                print(counter, seed12)
                counter += 1
                #Stop Button
                if not running:
                    break

                try:
                    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
                        symbol=ETH, account=0, change=False, address=0
                    )
                    bip44_hdwallet.from_mnemonic(mnemonic=seed12)
                    adr = bip44_hdwallet.address()
                    mnemo = bip44_hdwallet.mnemonic()
                    if adr.startswith(whole_address) and var.get() == 1:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed12}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        break
                    elif adr.startswith(beginning_of_the_address) and adr.endswith(end_of_the_address) and var.get() == 0:
                        print(60 * "=")
                        print("Seed Phrase Found!")
                        print(f"Seed Phrase: {mnemo}")
                        print("Address " + adr)
                        print(60 * "=")
                        a = (100*"=")
                        t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed12}\n{adr}\n{a}"))
                        t.see(END)
                        t.update()
                        scrollbar.update()
                        counter += 1
                        break
                except:
                    continue

    # Start Button
    start_button = tk.Button(buttons_frame, bg=background_color, fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", text="start", command=lambda: threading.Thread(target=MyClick).start())  # state=DISABLED <- Kada se doda ovo, dugme ne moze da se klikne
    start_button.grid(row=0, column=0, padx=5, pady=0, sticky="EN")
    # Stop Button
    stop_button = tk.Button(buttons_frame, bg=background_color, fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", text="stop", command=stop)
    stop_button.grid(row=0, column=1, padx=5, pady=0, sticky="WN")

    # Clear Button
    clear_button = tk.Button(instruction_frame, bg="#F2F2F2", fg="#0081C9", activebackground=background_color, activeforeground="#0081C9", text="clear", command=delete)
    clear_button.grid(row=6, column=1, pady=5)

    return tab2
