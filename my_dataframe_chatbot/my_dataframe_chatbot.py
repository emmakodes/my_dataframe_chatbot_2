import reflex as rx
from my_dataframe_chatbot.state import State


def head_text() -> rx.Component:
    """The header: return a text"""
    return rx.flex(
        rx.text("Chat with your data", size="4", align="center", weight="bold", color="white",),
            justify_content="center",
            width="100%",
            margin_bottom="5px"
    )


def confirm_upload() -> rx.Component:
    """text component to show upload confirmation."""
    return rx.chakra.text(State.upload_confirmation, text_align="center", font_weight="bold", color="green")  


def sidebar_drawer():
    """the sidebar component"""
    return rx.drawer.root(
            rx.drawer.trigger(rx.button("Open Drawer", position="fixed",)),
            rx.drawer.overlay(z_index="5"),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.flex(
                        rx.drawer.close(rx.box(rx.button("Close"))),
                        confirm_upload(),
                        head_text(),
                        rx.input(
                                placeholder="Enter Openai API key",
                                value=State.openai_api_key,on_change=State.set_openai_api_key,
                                width="22em",  
                                type="password",
                                ),
                        rx.vstack(
                            rx.upload(
                                rx.button("Select File", color="rgb(107,99,246)", bg="white", border=f"1px solid rgb(107,99,246)"),
                                rx.text("Drag and drop files here or click to select files"),
                                id="my_upload",
                                border="1px dotted rgb(107,99,246)",
                                padding="5em",
                                multiple=False,
                                accept = {
                                    "text/csv": [".csv"],  # CSV format
                                },
                                max_files=1,
                            ),                
                            margin_top="3px"
                        ),
                        rx.hstack(rx.foreach(rx.selected_files("my_upload"), rx.text)),
                        rx.button("Submit to start chat", variant="soft", margin_top="10px",on_click=lambda: State.handle_upload(
                            rx.upload_files(upload_id="my_upload")
                        ),),
                        direction="column",
                        align_items="start",
                        padding="0.2em",
                    ),
                    top="auto",
                    right="auto",
                    height="100%",
                    width="20em",
                    padding_left="0.2em",
                    background_color="#1a202c",
                    color="white",
                ),
                direction="left",
            )
        )


def error_text():
    """shown in case openai api key is not entered or file is not uploaded"""
    return rx.chakra.vstack(
        rx.chakra.modal(
            rx.chakra.modal_overlay(
                rx.chakra.modal_content(
                    rx.chakra.modal_body(
                        State.error_message
                    ),
                    rx.chakra.modal_footer(
                        rx.chakra.button(
                            "Close",
                            on_click=State.change,
                        )
                    ),
                )
            ),
            is_open=State.show,
        ),
    )


def skeleton_component() -> rx.Component:
    """Skeleton is used to display the loading state of some components."""
    return  rx.chakra.container(
                rx.chakra.skeleton_circle(
                            size="30px",
                            is_loaded=State.is_skeleton_loaded,
                            speed=1.5,
                            text_align="center",
                        ),  
                        display="flex",
                        justify_content="center",
                        align_items="center",
                    )


def qa(question: str, answer: str) -> rx.Component:
    """will show the question and answer"""
    return rx.box(
        rx.box(
            rx.text(question, text_align="right", color="black"),
            bg="#F5EFFE", margin_left="20%",
            padding="1em",border_radius="5px",
            margin_y="0.5em",box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
        ),
        rx.cond(
            answer,
                rx.box(
                    rx.text(answer, text_align="left", color="black"),
                    bg="#DEEAFD", margin_right="20%",
                    padding="1em",border_radius="5px",
                    margin_y="0.5em",box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
                ),
                rx.box()
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    """iterate over chat_history."""
    return  rx.box(
                rx.foreach(
                    State.chat_history,
                    lambda messages: qa(messages[0], messages[1]),
                ),
                skeleton_component(),
                py="8",
                flex="1",
                width="100%",
                max_width=  ["15em", "20em", "40em", "40em", "40em", "50em"],
                padding_x="4px",
                align_self="center",
                overflow="hidden",
                padding_bottom="5em",
                margin_left=["4em", "6em", "8em", "10em", "15em", "15em"]
    )


def hidden_button():
    """use the id to make the scrollbar be at its point, done so that the scrollbar to always be at the bottom"""
    return rx.flex(
                id="downloadbutton",
                background_color="black",
                color="black",
            )


def chat_content():
    return  rx.container(
                error_text(),
                chat(),
                hidden_button(),
            )


def input_question_box():
    """the input question box"""
    return  rx.flex(
                rx.text_area(
                    value=State.question,
                    placeholder="Ask a question about your data",
                    on_change=State.set_question,
                    width=["15em", "20em", "45em", "50em", "50em", "50em"],
                    color="white",
                    background_color="dark",
                    height="auto",
                ),
                rx.button(
                    rx.icon(
                        "send", 
                    ),
                    rx.box(
                        "Ask",
                        as_="span"
                    ),
                    on_click=State.answer,
                    size="2",
                    variant="solid",
                    color="white",
                ),
            direction="row",
            align="end",
            position="fixed",
            bottom="0",
            gap="8px",
            padding="16px",
            left="0",
            right="0",
            justify="center", 
            margin="auto",
            border_top=f"1px solid {rx.color('mauve', 3)}",
            background_color=rx.color("mauve", 2),
        )


def index() -> rx.Component:
  return rx.flex(
        sidebar_drawer(),
        chat_content(),
        input_question_box(),
        direction="row",
        gap="4px", 
        min_height="100vh",
        align_items="stretch",
        spacing="0",
  )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
    ),
)

app.add_page(index)