from tkinter import *
import tkinter as tk
from hdwallet import BIP44HDWallet
from hdwallet.symbols import ETH
from list import seeds
import itertools
import threading

def create_tab1(notebook):
    tab1 = tk.Frame(notebook)
    background_color = "#F1F6F5"
    tab1.config(bg=background_color)
    

    def pop_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    def copy():
        t.event_generate("<<Copy>>")

    def delete():
        words.delete(0, END)
        start_address_entry.delete(0, END)
        end_address_entry.delete(0, END)
        whole_address_entry.delete(0, END)

    def stop():
        global running
        running = False

    # Instruction Frame
    instruction_frame = tk.Frame(tab1, width=70, height=50, bg="#F2F2F2", highlightthickness=2, pady=20, padx=20, highlightbackground="#0081C9", highlightcolor="#0081C9")
    instruction_frame.grid(row=0, column=0, pady=20, padx=20)

    # Output Frame
    text_output_frame = tk.Frame(tab1, bg=background_color, highlightthickness=0, padx=30)
    text_output_frame.grid(row=3, column=0, pady=5)

    # Instructions
    main_description = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Enter the seed phrase, marking the unknown words with '???'.", font=("Arial", 13))
    main_description.grid(row=0, column=1)

    # Seed Phrase
    seed_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Seed Phrase Pattern: ")
    seed_label.grid(row=1, column=0)
    words = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=1)
    words.grid(row=1, column=1)

    # Start Address
    start_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Start of Address: ")
    start_address_label.grid(row=2, column=0)
    start_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    start_address_entry.grid(row=2, column=1)

    # End Address
    end_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="End of Address: ")
    end_address_label.grid(row=3, column=0)
    end_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    end_address_entry.grid(row=3, column=1)

    # Whole Address
    whole_address_label = tk.Label(instruction_frame, bg="#F2F2F2", fg="#0081C9", text="Whole Address: ")
    whole_address_label.grid(row=4, column=0)
    whole_address_entry = tk.Entry(instruction_frame, bg="#F2F2F2", fg="#0081C9", width=70, borderwidth=2, disabledbackground="#DBDBDB")
    whole_address_entry.grid(row=4, column=1)

    # Checkbox for enabling/disabling whole address input, or partial address input
    def Checked():
        if var.get() == 1:
            whole_address_entry.config(state=NORMAL)
            start_address_entry.config(state=DISABLED)
            end_address_entry.config(state=DISABLED)
        else:
            whole_address_entry.config(state=DISABLED)
            start_address_entry.config(state=NORMAL)
            end_address_entry.config(state=NORMAL)

    var = IntVar()
    checkbox_address = tk.Checkbutton(instruction_frame, bg="#F2F2F2", fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", highlightthickness=0, text="Whole Address/Partial Address", variable=var, command=Checked, onvalue=1, offvalue=0, border=None)
    checkbox_address.deselect()
    checkbox_address.invoke()
    checkbox_address.grid(row=5, column=1, sticky="W")

    # Text Output
    text_output_label = tk.Label(text_output_frame, bg=background_color, fg="#0081C9", text="Output:")
    text_output_label.grid(row=0, column=2)
    text_frame = tk.Frame(text_output_frame, background="yellow", width=100, height=90)
    text_frame.grid(row=1, column=2)
    scrollbar = tk.Scrollbar(text_frame)
    t = tk.Text(text_frame, bg="#F2F2F2", fg="#0081C9", highlightbackground="#0081C9", highlightcolor="#0081C9", height=10, width=100, yscrollcommand=scrollbar.set)
    scrollbar.config(command=t.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    t.pack()

    # Right Click menu
    menu = tk.Menu(t, tearoff=0, bg="black", fg="white")
    menu.add_command(label="Copy", command=copy)
    t.bind("<Button-3>", pop_menu)

    # Buttons frame
    buttons_frame = tk.Frame(tab1, width=300, height=20, bg=background_color, highlightthickness=0, pady=5, padx=20)
    buttons_frame.grid(row=4, column=0)

    def MyClick():
        global running
        running = True
        # getting input
        seed_phrase = words.get().strip()
        start_address = start_address_entry.get()
        end_address = end_address_entry.get()
        whole_address = whole_address_entry.get()

        num_replacements = seed_phrase.count("???")
        if num_replacements < 1 or num_replacements > 3:
            print("Unsupported number of ??? in the seed.")
            return

        # checking generated combinations
        comb = itertools.product(seeds, repeat=num_replacements)
        counter = 1

        for x in comb:
            if not running:
                break

            seed_modified = seed_phrase
            for word in x:
                seed_modified = seed_modified.replace("???", str(word), 1)

            print(counter, seed_modified)
            t.insert(END, (f"{counter} {seed_modified}\n"))
            t.see(END)
            t.update()
            scrollbar.update()
            counter += 1

            try:
                bip44_hdwallet = BIP44HDWallet(symbol=ETH, account=0, change=False, address=0)
                bip44_hdwallet.from_mnemonic(mnemonic=seed_modified)
                adr = bip44_hdwallet.address()
                mnemo = bip44_hdwallet.mnemonic()
                if (adr.startswith(start_address) and adr.endswith(end_address) and not var.get()) or (adr.startswith(whole_address) and var.get()):
                    print(60 * "=")
                    print("Seed Phrase Found!")
                    print(f"Seed Phrase: {mnemo}")
                    print("Address " + adr)
                    print(60 * "=")
                    a = 75 * "="
                    t.insert(END, (f"{a}\nSeed Phrase Found !!!\n{seed_modified}\n{adr}\n{a}"))
                    t.see(END)
                    t.update()
                    scrollbar.update()
                    break
            except:
                continue

    # Start Button
    start_button = tk.Button(buttons_frame, bg=background_color, fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", text="start", command=lambda: threading.Thread(target=MyClick).start())
    start_button.grid(row=0, column=0, padx=5, pady=0, sticky="EN")

    # Stop Button
    stop_button = tk.Button(buttons_frame, bg=background_color, fg="#0081C9", activebackground="#F2F2F2", activeforeground="#0081C9", text="stop", command=stop)
    stop_button.grid(row=0, column=1, padx=5, pady=0, sticky="WN")

    # Clear Button
    clear_button = tk.Button(instruction_frame, bg="#F2F2F2", fg="#0081C9", activebackground=background_color, activeforeground="#0081C9", text="clear", command=delete)
    clear_button.grid(row=5, column=1, pady=5)

    return tab1
