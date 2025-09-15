export type TextProps = {
    text: string,
    fontSize: number,
    colour?: string, // default colour is white
    fontFamily?: string, // default font is Arial
    backgroundColor?: string // default background is black
}

export const Text = (props: TextProps) => {
    const styles = {
        fontSize: `${props.fontSize}px`,
        color: props.colour || 'white',
        fontFamily: props.fontFamily || 'Arial',
        backgroundColor: props.backgroundColor || 'black'
    }

    return <h1 style={styles}>{props.text}</h1>;
}
