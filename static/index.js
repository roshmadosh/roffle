const textEditor = document.getElementById("text-editor");
let line1 = document.getElementById("line1");
const placeholder = document.getElementById("placeholder");


let line_number = 1;


line1.addEventListener("focusin", contentEditableEventHandler);
line1.addEventListener("focusout", contentEditableEventHandler);
line1.addEventListener("keydown", keydownEventHandler);


function contentEditableEventHandler(e) {
    const event = e.type;
    const lines = document.querySelectorAll('[contenteditable]');

    if (lines.length > 1) {
        return;
    }
    
    switch (event) {
        case 'focusin':       
            if (!line1.textContent) {
                placeholder.classList.add('invisible')
            } break;
        case 'focusout':
            if (!line1.textContent) {
                placeholder.classList.remove('invisible')
            } break;

        default:
            break;
        }
}

function keydownEventHandler(e) {
    
    const contentEditable = e.originalTarget;  
    const max_width = textEditor.offsetWidth * .87;

    const key = e.key;

    switch (key) {
        case 'Enter':
            createNewLine();
            return;
        case 'Backspace':
            if (!contentEditable.innerText) {
                removeLine()
            } return;
        default:
            break;
    }

    if (contentEditable.offsetWidth > max_width) { 
        e.preventDefault();
        createNewLine(); 
        return;
    }


}


function createNewLine() {
    line_number++;
    const breakline = document.createElement('br');
    breakline.setAttribute('id', `breakline${line_number}`);
    const newline = document.createElement('span');
    newline.setAttribute('id', `line${line_number}`);
    newline.setAttribute('contenteditable', 'true');

    textEditor.appendChild(breakline);
    textEditor.appendChild(newline)
    
    newline.addEventListener("keydown", keydownEventHandler);
    newline.focus();
}

function removeLine() {

    const breakline = document.getElementById(`breakline${line_number}`);
    const prevLine = document.getElementById(`line${line_number - 1}`)
    const line = document.getElementById(`line${line_number}`);
    breakline.remove()
    line.remove();


    prevLine.focus();

}