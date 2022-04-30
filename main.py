from tkinter import *
from tkinter import scrolledtext
import math
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
    n = n_text.get("1.0", 'end-1c')
    if not n.isdigit() or int(n) == 1:
        return p_text.insert(END, "Введен некорректный символ")
    x_1 = 150
    p = factor_rho(int(n), x_1)
    print("p =", p)
    q = int(int(n) / p)

    p_text.insert(END, str(p))
    q_text.insert(END, str(q))


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
    message = ''
    dictionary = {}
    total = 16
    for i in range(1040, 1104):
        dictionary[chr(i)] = total
        total += 1
    fn = (p - 1) * (q - 1)
    d = mulinv(int(e), fn)
    int_message = power(int(sw), d, n)
    print(int_message)
    int_message %= 64
    if int_message < 16:
        int_message += 64
    if int_message > 79:
        int_message -= 64
    for k, v in dictionary.items():
        if int_message == v:
            message = k
            break
        else:
            message = 'Сообщение не расшифровывается'

    fn_text.insert(END, str(fn))
    d_text.insert(END, str(d))
    result_int_text.insert(END, str(int_message))
    result_alphabet_text.insert(END, str(message))


def insert_text():
    n_text.delete('1.0', END)
    e_text.delete('1.0', END)
    sw_text.delete('1.0', END)
    number = variant_text.get("1.0", 'end-1c')
    if not number.isdigit():
        return n_text.insert(END, "Введен некорректный символ")
    if int(number) > 75 or int(number) < 1:
        return n_text.insert(END, "Такого варианта нет")
    doc = docx.Document('Labs_IBKS_2018_1.docx')
    text = []
    d = {}
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    text_1 = '\n'.join(text)[21231:30067].strip()
    a = text_1.split('\n')
    print(text_1)
    for i in range(1, len(a), 2):
        d[a[i - 1]] = a[i]

    print(a)
    print(d)
    dy = {}
    for k, v in d.items():
        arr = []
        k = k.replace('Вариант ', '').strip()
        v = v.strip().split(',')
        for i in v:
            i = i.strip()
            i = i.replace('n=', '')
            i = i.replace('e=', '')
            i = i.replace('SW=', '')

            arr.append(i)
        dy[k] = arr
        if number == k:
            n_text.insert(END, arr[0])
            e_text.insert(END, arr[1])
            sw_text.insert(END, arr[2])


window = Tk()

window.title("factorization of the RSA key")
window.geometry("1920x1080")

heading = Label(window, text="factorization of the RSA key", font=("Terminal", 35))
heading.pack(expand=False, fill=NONE)

n_ui = Label(window, text="n:", font=("Terminal", 25))
n_ui.place(x=10, y=100, height=80, width=40)
n_text = scrolledtext.ScrolledText(window, width=40, height=10)
n_text.place(x=70, y=110, height=60, width=300)
hack_btn = Button(window, text="Hack", font=("Arial Bold", 15), bg="black", fg="white", command=test_factor_rho)
hack_btn.place(x=210, y=200, anchor="center", height=30, width=180, bordermode=OUTSIDE)
p_ui = Label(window, text="p:", font=("Terminal", 25))
p_ui.place(x=10, y=240, height=80, width=40)
p_text = scrolledtext.ScrolledText(window, width=40, height=10)
p_text.place(x=70, y=250, height=60, width=300)
q_ui = Label(window, text="q:", font=("Terminal", 25))
q_ui.place(x=10, y=330, height=80, width=40)
q_text = scrolledtext.ScrolledText(window, width=40, height=10)
q_text.place(x=70, y=340, height=60, width=300)
e = Label(window, text="e:", font=("Terminal", 25))
e.place(x=500, y=100, height=80, width=40)
e_text = scrolledtext.ScrolledText(window, width=40, height=10)
e_text.place(x=560, y=110, height=60, width=300)
sw_ui = Label(window, text="sw:", font=("Terminal", 25))
sw_ui.place(x=500, y=190, height=80, width=55)
sw_text = scrolledtext.ScrolledText(window, width=40, height=10)
sw_text.place(x=560, y=200, height=60, width=300)
decode_btn = Button(window, text="Decode the message", font=("Arial Bold", 15), bg="black", fg="white", command=decode)
decode_btn.place(x=700, y=290, anchor="center", height=30, width=200, bordermode=OUTSIDE)
fn_ui = Label(window, text="φ(n):", font=("Arial Bold", 18))
fn_ui.place(x=500, y=330, height=80, width=55)
fn_text = scrolledtext.ScrolledText(window, width=40, height=10)
fn_text.place(x=560, y=340, height=60, width=300)
d_ui = Label(window, text="d:", font=("Terminal", 25))
d_ui.place(x=500, y=420, height=80, width=55)
d_text = scrolledtext.ScrolledText(window, width=40, height=10)
d_text.place(x=560, y=430, height=60, width=300)
result_ui = Label(window, text="Result:", font=("Terminal", 23))
result_ui.place(x=630, y=500, height=30, width=140)
result_int_text = scrolledtext.ScrolledText(window, width=40, height=10)
result_int_text.place(x=560, y=550, height=60, width=300)
result_alphabet_text = scrolledtext.ScrolledText(window, width=40, height=10)
result_alphabet_text.place(x=560, y=640, height=60, width=300)

variant = Label(window, text="Вариант:", font=("Aria Bold", 12))
variant.place(x=10, y=10, height=80, width=65)
variant_text = scrolledtext.ScrolledText(window, width=40, height=10)
variant_text.place(x=90, y=30, height=40, width=120)
insert_btn = Button(window, text="Insert", font=("Arial Bold", 15), bg="black", fg="white", command=insert_text)
insert_btn.place(x=280, y=50, anchor="center", height=30, width=100, bordermode=OUTSIDE)
window.mainloop()