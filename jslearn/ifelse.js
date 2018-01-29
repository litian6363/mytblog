'use strict';

var height = parseFloat(prompt('请输入身高(m):'));
var weight = parseFloat(prompt('请输入体重（kg）：'));

var bmi = weight / (height * height);
if (bmi < 18.5){
    console.log('过轻')
}else if (18.5 <= bmi < 25){
    console.log('正常')
}else if (25 <= bmi < 28){
    console.log('过重')
}else if (28 <= bmi < 32){
    console.log('肥胖')
}else if (32 <= bmi){
    console.log('严重肥胖')
}
