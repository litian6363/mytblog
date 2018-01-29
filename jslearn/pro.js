'user strict'
// 全局变量都在 window 对象里
function ofWindow (){
    var v;
    for (v in window){ 
        console.log(v)
    }
}
ofWindow();

// 声明常量
const PI = 3.14;
PI = 3;
PI;