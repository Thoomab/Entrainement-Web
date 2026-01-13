let cliqueAvant = []
let cliqueApres = []
let i = 0
let operator
let total

function appuieTouche(idDuBouton){
    var button = document.getElementById(idDuBouton).textContent;
    var result = document.getElementById("affichage");

        switch (button) {
            case "C":
                console.log("C")
                result.value = "";
                cliqueAvant = [];
                cliqueApres = [];
                operator = null
                total = 0;
                break;
            
            case "/":
                console.log("/")
                operator = cliqueAvant.length
                console.log(operator)
                cliqueAvant.push(button)

                if (cliqueAvant[0] == "/"){
                    alert("Veuillez d'abord entrez un chiffre/nombre !")
                    result.value = "";
                    cliqueAvant = [];
                    cliqueApres = [];
                    operator = null
                    total = 0;
                }else{
                    result.value += ' ' + "/"  + ' '
                }

                break;

            case "*":
                console.log("*")
                operator = cliqueAvant.length
                console.log(operator)
                cliqueAvant.push(button)
                
                if (cliqueAvant[0] == "*"){
                    alert("Veuillez d'abord entrez un chiffre/nombre !")
                    result.value = "";
                    cliqueAvant = [];
                    cliqueApres = [];
                    operator = null
                    total = 0;
                }else{
                    result.value += ' ' + "*"  + ' '
                }

                break;

            case "-":
                console.log("-")
                operator = cliqueAvant.length
                console.log(operator)
                cliqueAvant.push(button)

                if (cliqueAvant[0] == "-"){
                    alert("Veuillez d'abord entrez un chiffre/nombre !")
                    result.value = "";
                    cliqueAvant = [];
                    cliqueApres = [];
                    operator = null
                    total = 0;
                }else{
                    result.value += ' ' + "-"  + ' '
                }
                break;

            case "+":
                console.log("+")
                operator = cliqueAvant.length
                console.log(operator)
                cliqueAvant.push(button)

                if (cliqueAvant[0] == "+"){
                    alert("Veuillez d'abord entrez un chiffre/nombre !")
                    result.value = "";
                    cliqueAvant = [];
                    cliqueApres = [];
                    operator = null
                    total = 0;
                } else{
                    result.value += ' ' + "+"  + ' '
                }
                break;

            case "=":
                console.log("=")
                totUn = cliqueAvant.join("")
                totDeux = cliqueApres.join("")

                if (cliqueAvant[operator] === "+"){
                    total = parseFloat(totUn) + parseFloat(totDeux)
                }
                else if (cliqueAvant[operator] === "-"){
                    total = parseFloat(totUn) - parseFloat(totDeux)
                }
                else if (cliqueAvant[operator] === "*"){
                    total = parseFloat(totUn) * parseFloat(totDeux)
                }
                else if (cliqueAvant[operator] === "/"){
                    total = parseFloat(totUn) / parseFloat(totDeux)
                }
                result.value = total
                break;
        
            default:
                if (cliqueAvant[operator] == "+" || cliqueAvant[operator] == "-" || cliqueAvant[operator] == "*" || cliqueAvant[operator] == "/"){
                    cliqueApres.push(button)
                    console.log(cliqueApres)
                    result.value += button;
                    i++;
                } else {
                    cliqueAvant.push(button)
                    console.log(cliqueAvant)
                    result.value += button;
                    i++;
                }
                
                break;
        }
    }