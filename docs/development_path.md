# Project Development Considerations

## Project Origins and Motivation

This project was born from the desire to showcase on my curriculum a project that would demonstrate, first and foremost, my **dedication** to studying new technologies and applying them promptly. In reality, as I'll explain better throughout these lines, the project I created was somewhat like using the handle of a screwdriver as a hammer. However, the real purpose was to take an idea and create it with a specific programming language without fear of project scalability or new technologies to implement. This led me to make many decisions that, one way or another, made the project increasingly complex as time passed. But let's proceed in order.

Once I decided to learn Python, one week after familiarizing myself with the language, I thought it would be good to create this project: a CRUD application that would allow users to manage monetary transactions. Something small but useful, which many people generally do in Excel, myself included. So the idea was born from a real need for something useful, and initially, the concept was to create something that included only transactions and perhaps some trend charts.

I'll anticipate that once the project was finished (or almost), I understood Python's potential and how this project is possible and functional in Python, but it's not the best way to create an application of this kind. This is for several reasons. Python is a very powerful language; it's extremely easy and allows creating functional applications with simple-to-read syntax. It's also very versatile for web scraping, data science, automation, AI, and more. Finally, it has an enormous community and libraries for all tastes, as well as the possibility of being deployed on various different platforms. However, for CRUD applications, as I mentioned earlier, using it is not very intelligent. Python is also very slow for its operations, and the fact that it's single-threaded prevents the interactivity of such applications, not to mention the very high memory cost. In the case of the application itself, tkinter appears very outdated visually, and although customtkinter marginally solves the problem, there's no simple way at the GUI and interface level to create visually appealing, modern, and useful widgets. Furthermore, since these are internal to the code, they make the code thousands of lines long due to how tkinter works.

So Python isn't the best way to make CRUD applications and the GUI appears outdated, so why did I do it? Very simply, I realized this ouroboros during the first 30 commits, so unfortunately I was too deep to abandon it. Therefore, I decided to continue to push the project to its maximum and learn from it. For this reason, at a certain point, I decided to make it more complex by using design patterns and local databases, etc.

For advice on what types of technologies to use for CRUD applications, these are generally perfect:
- **Web-based**: React/Vue + Node.js/Django/FastAPI for modern web UIs
- **Desktop**: Electron, Flutter, or native apps (C#/.NET, Swift, Kotlin)

If I were to dabble in another application like this in the future, I would probably go with web-based.

## Refactoring

After the first 30 commits and after effectively creating the user settings screen, a theme selection screen, and the home page, it was decided to refactor.

To improve the program's scalability as well as readability and comprehension, it was decided to perform timely code refactoring, focusing on compartmentalization and extraction of components that made files too long. An emblematic example of this problem is the app.py file, which manages the GUI and therefore represents the backbone of the graphical interface.

Due to the nature of customtkinter (or tkinter itself), the file contains a relatively substantial number of lines of code despite including only three frames. To further improve its readability, the next refactoring steps involve extracting these frames into separate files, thus obtaining code that—although more dispersive due to the increased number of files—is cleaner, simpler to read, and consistent with the professionalism expected from a proprietary application.

At certain times I found myself deciding whether to insert comments or not, but I tried to make my code as understandable as possible, so many times I opted to avoid commenting on understandable functions. Regarding custom tkinter, more than what I wrote was impossible for me to do. Python's graphical UI libraries, from what I've seen, are not optimized and require an enormous amount of lines of code for even simple things in other environments like web development. For this reason, much of the GUI work was trial and error with external help from Claude Sonnet, which was essential given the poor documentation of custom tkinter compared to its derivative.

A design choice that might prove unpopular is how I handled settings.py, a list of constants used throughout the program that allow modifying the program's behavior conveniently from a single file at any time. I believe and hope this won't be cause for disputes, but how I handled the default user settings, creating constants for both keys and default values, might seem quite strange. The motivation behind this choice is simply wanting to avoid typo problems in the code, using constants that are recognized and immediately flagged. At the end of the project, I want to run speed tests to understand if this slowed down the application, but for now, I believe it's a fair compromise for code readability and comprehension, an objective I decided to put first.

Let's be clear: this project is quite simple logically—it's a CRUD application (CREATE, READ, UPDATE, and DELETE), and the most difficult part is conceiving the GUI rendering. However, my desire to show my determination in learning, understanding, and applying serious and professional work methodologies is what distinguishes this project. Many of the choices made weren't necessary for the project to function and do what it should do, but the flame of showing and presenting a project with documentation, file structure, and clean code writing pushed me to create the project as shown here. **I'm aware I didn't fully succeed and perhaps made many mistakes, but being my first project outside university, on topics that were never covered in university or covered too superficially, well, it makes me proud of what I've done.**

## Why SQLite

I chose to use SQLite as the data management system for this project because it offers a robust, efficient, and scalable solution while maintaining simple and lightweight configuration. Compared to a CSV file-based approach, SQLite guarantees greater data integrity, allowing me to define types, constraints, and complex queries safely and performantly. This allows me to sort, filter, and manage transactions much more efficiently, avoiding the need to implement manual logic in Python for common operations. Additionally, SQLite is easily integrable into the project without requiring external dependencies, maintaining portability and ease of use, but with the robustness necessary to support future expansions such as introducing multiple tables, categories, or statistics.

Export and import, however, occurs through CSV files because they're easily modifiable by the user. These are translated into the database when imported.

## Project Challenges

Personally, the most frustrating part of the project was the GUI. It's the component that required the project to last so long, and if everything had been done in CLI, I would probably be working on another project by now. Beyond this—I'll address the topic better later—I found myself several times asking about the best approach for implementing a specific feature, and here AI was of great help.

## AI Usage

Let's start with the simplest part: everything textual in this project was written by me 90% in English and then grammatically corrected by the two artificial intelligences I used, ChatGPT and Claude Sonnet. I want to say this because, although I have an almost perfect understanding of English in listening and reading (I watch stuff without subtitles now), writing and speaking, being little practiced, are notably lower quality. Therefore, I often found myself writing what I wanted to say in English but in imperfect verbal forms that needed external correction. Additionally, I decided to use English because I've been writing code in English for as long as I can remember, and therefore it seemed right that the documentation should be as well.

Now let's talk about AI's help on the project. For this project, AI was used less and less as time passed, and after the first 30 commits and the refactoring done, AI usage reached its minimum. For quick information retrieval, like SQLite or CSV, I generally preferred a video that illustrated the entire process to me. This helped me understand the information better. For technical questions, I approached AI with the intent to understand and better comprehend what to do and what was right to do. I don't know if this is the best method to use it, but I found myself several times having a problem and thinking of a solution that would involve writing ugly code. In those cases, I explained the situation and asked for the best approaches without providing code, because I wanted to understand what to implement. In these cases, then I went back and forth to implement the solution, trying to understand the workings elsewhere too. For example, the callback function was proposed by Claude Sonnet, as was the design pattern—elements that unfortunately I didn't fully know and that I wanted to implement because they seemed right for this application, and so it was.

Another element for which AI was useful was understanding GUI functionality and creating some widgets I didn't understand how to create. As with the rest, I used AI less and less, and from about mid-project I started using it little for this purpose. But tkinter and customtkinter are complex, and having thrown myself into the project with only examples of other code provided by customtkinter and the documentation, I didn't have the material time to learn it properly. Therefore, several gaps led me to make errors that AI helped me correct.

As a programmer, I found myself using AI for a project for the first time, and I must say it's frighteningly powerful—perhaps too powerful. If prompts aren't precise and limiting, AIs tend to give you more than you ask for, then you find yourself not understanding the code you've written and how it works. Yes, the application works, but at what price if you don't know how it functions?

One thing for which I believe AI is an excellent breakthrough and for which I don't feel guilty about using is debugging and possible problems that can emerge from code. It's something I used little, but it seems like just saved time, although I'm afraid that doing it for too long might lead to code simplification because you're sure AI can fix it.

I found myself understanding during this project how incredibly useful AI is as a tool, but you must be cautious. Copying and pasting code after it gives you the solution is palliative for the programmer themselves. I believe that in the future, as I also did in the last part of this project, I will limit the code that AI provides me and use it more as one of the sources instead of the only source. This is to create a curriculum of more practical and solid programming experiences.

Like every tool of this kind, the answer lies in moderation.

----------
