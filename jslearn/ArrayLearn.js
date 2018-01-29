'user strict'
var arr = ['小明', '小红', '大军', '阿黄'];
arr = arr.sort();
var length = '999';
length = arr.length;
var arrf = arr.slice(0,length-1).join(',');
console.log('欢迎' + arrf + '和' + arr.slice(length-1));