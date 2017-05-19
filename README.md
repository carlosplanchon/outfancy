# outfancy

*Table printing in Terminal*

[![Join the chat at https://gitter.im/carlosplanchon/outfancy](https://badges.gitter.im/carlosplanchon/outfancy.svg)](https://gitter.im/carlosplanchon/outfancy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

<img src='examples/chart_auto.png'>

##Demonstration
- http://showterm.io/42f0bfa286232758acf18
- http://showterm.io/5a31927cbfdc37e116f8d

## what is it?
Outfancy is a python library to print tables in Terminal. It's a quick way to visualize data when you don't have a GUI and can be integrated easily in your programs. It's written in python3 and can quickly be installed anywhere using pip3.

## installation
### install with pip3
```
$ pip3 install outfancy
```

## features

- Quick printing of tables.
- customize the separator used, width, priority of printing for each column.
- rearrange the columns in real time.
- Add labels above the table (can be autogenerated).
- Do Oneline printing, useful for real-time applications (report in screen function).
- Add colors to the field of the tables.
<img src='examples/colors_supported.png'>


## usage
### In the interpreter
```
import outfancy
motor = outfancy.render.Table()
some_data = [(1, 'Foo'), (2, 'Bar')]
print(motor.render(some_data))
```

## To do (Colaboration is welcome)
- Translate code to english. (Translated) (the translation need revision from a native english speaker (I speak spanish).
- color option. (Added) (Can be improved using regex (see widgets.py))
- Add basic charting functions (in the folder code_to_use i have some code found in internet that can be used to that functions).

## Others
- https://gist.github.com/carlosplanchon/986c7c11a932a7206bb3 (Funny demo with colors)

## Experimental (Line plot)
<img src='examples/sin_little.png'>
- http://showterm.io/80074a1806e78205339d6
