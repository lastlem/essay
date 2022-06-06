from tkinter import *
from tkinter.ttk import *
import time


def count_written_sentences(written_text: str) -> int:
    sentences_end_with_dot = len(written_text.split('.')) - 1
    sentences_end_with_question_mark = len(written_text.split('?')) - 1
    sentences_end_with_exclamation_mark = len(written_text.split('!')) - 1
    sentences = sentences_end_with_dot + sentences_end_with_question_mark + sentences_end_with_exclamation_mark
    return sentences


def count_written_words(event) -> int:
    full_text = '{0}{1}'.format(text.get(1.0, END).replace('\n', ''), event.char)
    return len(full_text.split())


def count_written_sentences_in_passage(passage) -> int:
    sentences_in_start = text.get(1.0, END).split('\n')
    if passage > len(sentences_in_start) - 1:
        return 0
    sentences_in_start = sentences_in_start[passage]
    return count_written_sentences(sentences_in_start)


def get_status(event):
    label_written_words['text'] = f'Written words: {count_written_words(event)}'
    label_written_sentences['text'] = f'Written sentences: {count_written_sentences(text.get(1.0, END))}'
    label_written_sentence_start['text'] = f'Written start sentences: {count_written_sentences_in_passage(0)}'
    label_written_sentence_main['text'] = f'Written main sentences: {count_written_sentences_in_passage(1)}'
    label_written_sentence_end['text'] = f'Written end sentences: {count_written_sentences_in_passage(2)}'


def count_sentences(word_limit: int, words_in_sentence: int) -> tuple:
    sentence_total = word_limit // words_in_sentence
    sentence_main = sentence_total // 2
    sentence_start_end = sentence_main // 2
    return sentence_start_end, sentence_main


def get_task_variables():
    words_min = entry_min_words.get().strip()
    words_max = entry_max_words.get().strip()
    sentence_len = entry_sentence_len.get().strip()
    return words_min, words_max, sentence_len


def to_int(inputs):
    return (int(element) for element in inputs)


def is_int(inputs):
    for element in inputs:
        if not element.isdigit():
            return False
    return True


def get_task(event) -> None:
    if not is_int(get_task_variables()):
        return

    words_min, words_max, sentence_len = to_int(get_task_variables())

    sentence_start_end_min, sentence_main_min = count_sentences(words_min, sentence_len)
    sentence_start_end_max, sentence_main_max = count_sentences(words_max, sentence_len)

    label_sentence_start.config(text=f"Number of start sentences: {sentence_start_end_min} - {sentence_start_end_max}")
    label_sentence_main.config(text=f"Number of start sentences: {sentence_main_min} - {sentence_main_max}")
    label_sentence_end.config(text=f"Number of start sentences: {sentence_start_end_min} - {sentence_start_end_max}")


def set_result(event):
    min_words = entry_min_words.get()
    max_words = entry_max_words.get()

    if not is_int((min_words, max_words)):
        return

    min_words, max_words = to_int((min_words, max_words))
    written_words = count_written_words(event)
    if written_words < min_words:
        label_result['text'] = 'Result: Less...'
    elif min_words <= written_words <= max_words:
        label_result['text'] = 'Result: Ready!'
    else:
        label_result['text'] = 'Result: Much...'


def get_time_string(seconds: int) -> str:
    hour = seconds // 3600
    minute = seconds // 60 % 60
    second = seconds % 60
    return f'Spent time: {hour:02}:{minute:02}:{second:02}'


def tick(time_from: int):
    real_time = round(time.time())
    total_seconds = real_time - time_from
    label_time_spent.config(text=get_time_string(total_seconds))
    if not label_result['text'] == 'Result: Ready!':
        label_time_spent.after(1000, tick, time_from)


def set_time(event):
    time_from = round(time.time())
    tick(time_from)
    text.unbind('<FocusIn>')


root = Tk()
root.title('Literary note')

text = Text(wrap=WORD, width=30)
text.pack(side=LEFT, expand=1, fill=BOTH)
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

frame_right = Frame()
frame_right.pack(side=LEFT, fill=Y)

frame_task = LabelFrame(frame_right, text='Task:')
frame_task.pack(fill=X)

Label(frame_task, text='Min words:').pack()
entry_min_words = Entry(frame_task, justify=RIGHT)
entry_min_words.insert(END, 20)
entry_min_words.pack(fill=X)

Label(frame_task, text='Max words:').pack()
entry_max_words = Entry(frame_task, justify=RIGHT)
entry_max_words.insert(END, 30)
entry_max_words.pack(fill=X)

Label(frame_task, text='Number of words in a sentence:').pack()
entry_sentence_len = Entry(frame_task, justify=RIGHT)
entry_sentence_len.insert(END, 2)
entry_sentence_len.pack(fill=X)

label_sentence_start = Label(frame_task, text="Number of start sentences: 2 - 3")
label_sentence_start.pack(fill=X)
label_sentence_main = Label(frame_task, text="Number of main sentences: 5 - 7")
label_sentence_main.pack(fill=X)
label_sentence_end = Label(frame_task, text="Number of end sentences: 2 - 3")
label_sentence_end.pack(fill=X)

frame_status = LabelFrame(frame_right, text='Status:')
frame_status.pack(fill=X)
label_written_words = Label(frame_status, text='Written words: 0')
label_written_words.pack(fill=X)
label_written_sentences = Label(frame_status, text='Written sentences: 0')
label_written_sentences.pack(fill=X)

label_written_sentence_start = Label(frame_status, text="Written start sentences: 0")
label_written_sentence_start.pack(fill=X)
label_written_sentence_main = Label(frame_status, text="Written main sentences: 0")
label_written_sentence_main.pack(fill=X)
label_written_sentence_end = Label(frame_status, text="Written end sentences: 0")
label_written_sentence_end.pack(fill=X)

frame_result = LabelFrame(frame_right, text='Result:')
frame_result.pack(fill=X)
label_time_spent = Label(frame_result, text='Spent time: 00:00:00')
label_time_spent.pack(fill=X)
label_result = Label(frame_result, text="Result: Less.../Ready!/Much...")
label_result.pack(fill=X)

root.bind("<Return>", get_task)
text.bind('<Key>', get_status)
text.bind('<Key>', set_result, add='+')
text.bind('<FocusIn>', set_time)
root.mainloop()
