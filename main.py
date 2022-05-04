import math
import time

from tkinter import *
from tkinter import scrolledtext
import docx


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:

        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p

    return res


def f(x):
    return x ** 2 + 1


def factor_rho(n, x_1):
    x = x_1
    xp = f(x) % n
    p = math.gcd(x - xp, n)

    while p == 1:
        # in the ith iteration x = x_i and x' = x_2i
        x = f(x) % n
        xp = f(xp) % n
        xp = f(xp) % n
        p = math.gcd(x - xp, n)

    if p == n:
        return -1
    else:
        return p


def test_factor_rho():
    p_text.delete('1.0', END)
    q_text.delete('1.0', END)
    time_po_without_threads.delete('1.0', END)
    n = n_text.get("1.0", 'end-1c')
    if not n.isdigit() or int(n) == 1:
        return p_text.insert(END, "Введен некорректный символ")

    x_1 = 150
    start_time = time.time()
    p = factor_rho(int(n), x_1)
    execution_time = time.time() - start_time
    print("p =", p)
    q = int(int(n) / p)

    p_text.insert(END, str(p))
    q_text.insert(END, str(q))
    time_po_without_threads.insert(END, f'{str(execution_time)} seconds')


def decode():
    fn_text.delete('1.0', END)
    d_text.delete('1.0', END)
    result_int_text.delete('1.0', END)
    result_alphabet_text.delete('1.0', END)
    e = e_text.get("1.0", 'end-1c')
    sw = sw_text.get("1.0", 'end-1c')
    n = int(n_text.get("1.0", 'end-1c'))
    p = int(p_text.get("1.0", 'end-1c'))
    q = int(q_text.get("1.0", 'end-1c'))

    if not e.isdigit() or not sw.isdigit():
        return result_alphabet_text.insert(END, "Введен некорректный символ")

    dictionary = {}
    total = 16
    message = ''

    for i in range(1040, 1104):
        dictionary[chr(i)] = total
        total += 1

    print(dictionary)

    fn = (p - 1) * (q - 1)
    d = mulinv(int(e), fn)
    int_message = power(int(sw), d, n)
    print(int_message)
    arr = []
    for i in range(1, len(str(int_message)), 2):
        arr.append(str(int_message)[i - 1] + str(int_message)[i])
    print(arr)

    for i in range(len(arr)):
        for k, v in dictionary.items():
            if arr[i] == str(v):
                print(arr[i])
                print(str(v))

                message += k
                print(message)
                break

    fn_text.insert(END, str(fn))
    d_text.insert(END, str(d))
    result_int_text.insert(END, str(int_message))
    result_alphabet_text.insert(END, str(message))


def insert_text():
    n_text.delete('1.0', END)
    e_text.delete('1.0', END)
    sw_text.delete('1.0', END)
    p_text.delete('1.0', END)
    q_text.delete('1.0', END)
    time_po_without_threads.delete('1.0', END)
    fn_text.delete('1.0', END)
    d_text.delete('1.0', END)
    d_text.delete('1.0', END)
    result_int_text.delete('1.0', END)
    result_alphabet_text.delete('1.0', END)
    number = variant_text.get("1.0", 'end-1c')

    if not number.isdigit():
        return n_text.insert(END, "Введен некорректный символ")
    if int(number) > 75:
        return n_text.insert(END, "Такого варианта нет")

    doc = docx.Document('Labs_IBKS_2018_1.docx')
    text = []
    d = {}
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    text = '\n'.join(text)
    start_text = text.index('Вариант 1')
    end_text = text.index('\n\n\nЛабораторная работа №3')
    text = text[start_text:end_text].strip().split('\n')

    for i in range(1, len(text), 2):
        d[text[i - 1]] = text[i]

    for k, v in d.items():
        k = k.replace('Вариант ', '').strip()
        if number == k:
            result_list = []
            v = v.strip().split(',')
            for i in v:
                i = i.strip()
                i = i.replace('n=', '')
                i = i.replace('e=', '')
                i = i.replace('SW=', '')
                result_list.append(i)
            n_text.insert(END, result_list[0])
            e_text.insert(END, result_list[1])
            sw_text.insert(END, result_list[2])
            break


window = Tk()

window.title("factorization of the RSA key")
window.geometry("1920x1080")
window.configure(bg='black')

heading = Label(window, text="factorization of the RSA key", font=("Terminal", 35), bg='black', fg='white')
heading.pack(expand=False, fill=NONE)


variant = Label(window, text="Variant:", font=("Terminal", 12), bg='black', fg='white')
variant.place(x=10, y=10, height=80, width=80)
variant_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
variant_text.place(x=100, y=30, height=40, width=120)
insert_btn = Button(window, text="Insert", font=("Arial Bold", 15), bg="black", fg="white", command=insert_text)
insert_btn.place(x=280, y=50, anchor="center", height=30, width=100, bordermode=OUTSIDE)


n_ui = Label(window, text="n:", font=("Terminal", 25), bg='black', fg='white')
n_ui.place(x=10, y=100, height=80, width=40)
n_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
n_text.place(x=70, y=110, height=60, width=335)
hack_btn = Button(window, text="Hack", font=("Arial Bold", 15), bg="black", fg="white", command=test_factor_rho)
hack_btn.place(x=235, y=200, anchor="center", height=30, width=180, bordermode=OUTSIDE)


p_ui = Label(window, text="p:", font=("Terminal", 25), bg='black', fg='white')
p_ui.place(x=10, y=240, height=80, width=40)
p_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
p_text.place(x=70, y=250, height=60, width=335)
q_ui = Label(window, text="q:", font=("Terminal", 25), bg='black', fg='white')
q_ui.place(x=10, y=330, height=80, width=40)
q_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
q_text.place(x=70, y=340, height=60, width=335)
time_po_without_threads = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black',
                                                    font=("Terminal", 5))
time_po_without_threads.place(x=70, y=430, height=60, width=335)


e_ui = Label(window, text="e:", font=("Terminal", 25), bg='black', fg='white')
e_ui.place(x=500, y=100, height=80, width=40)
e_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
e_text.place(x=560, y=110, height=60, width=335)
sw_ui = Label(window, text="sw:", font=("Terminal", 25), bg='black', fg='white')
sw_ui.place(x=500, y=190, height=80, width=55)
sw_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
sw_text.place(x=560, y=200, height=60, width=335)
decode_btn = Button(window, text="Decode the message", font=("Arial Bold", 15), bg="black", fg="white", command=decode)
decode_btn.place(x=725, y=290, anchor="center", height=30, width=200, bordermode=OUTSIDE)


fn_ui = Label(window, text="φ(n):", font=("Arial Bold", 18), bg='black', fg='white')
fn_ui.place(x=500, y=330, height=80, width=55)
fn_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
fn_text.place(x=560, y=340, height=60, width=335)
d_ui = Label(window, text="d:", font=("Terminal", 25), bg='black', fg='white')
d_ui.place(x=500, y=420, height=80, width=55)
d_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
d_text.place(x=560, y=430, height=60, width=335)
result_ui = Label(window, text="Result:", font=("Terminal", 23), bg='black', fg='white')
result_ui.place(x=655, y=500, height=30, width=140)
result_int_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black', font=("Terminal", 5))
result_int_text.place(x=560, y=550, height=60, width=335)
result_alphabet_text = scrolledtext.ScrolledText(window, width=40, height=10, bg='#F0F8FF', fg='black',
                                                 font=("Terminal", 5))
result_alphabet_text.place(x=560, y=640, height=60, width=335)

window.mainloop()
