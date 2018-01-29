'use strict'

// 题一：reduce乘积练习
function product(arr){
    return arr.reduce(function(x, y){
        return x * y;
    });
}
// 测试:
if (product([1, 2, 3, 4]) === 24 && product([0, 1, 2]) === 0 && product([99, 88, 77, 66]) === 44274384) {
    console.log('测试通过!');
}
else {
    console.log('测试失败!');
}

// 题二：字符串转数字
function string2int(s){
    var slist = [];
    var k;
    for(k of s){
        slist.push(k);
    }
    var m = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9};
    var smap = slist.map(function ch(x){
        return m[x];
    });
    return smap.reduce(function(n1, n2){
        return n1 * 10 + n2;
    });
}
//console.log(string2int('0'));
// 测试:
if (string2int('0') === 0 && string2int('12345') === 12345 && string2int('12300') === 12300) {
    if (string2int.toString().indexOf('parseInt') !== -1) {
        console.log('请勿使用parseInt()!');
    } else if (string2int.toString().indexOf('Number') !== -1) {
        console.log('请勿使用Number()!');
    } else {
        console.log('测试通过!');
    }
}
else {
    [string2int('0'), string2int('12345'), string2int('12300')].map(console.log);
    console.log('测试失败a!');
}

// 题三：
function normalize(arr){
    var low = arr.map(function(s){
        return s.toLowerCase();
    });
    var ss = low.map(function(s){
        return s[0] = s[0].toUpperCase();     
    });
    return ss;
}
var a = ['adam', 'LISA', 'barT'];
console.log(normalize(a));