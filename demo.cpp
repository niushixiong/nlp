#include <Python.h>
using namespace std;
int main(int argc, char* argv[])
{
    test();
    test1();
    test2();
 

    return 0;
}
void getcurrent()
{
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");
    return;
}
void test()
{
    Py_Initialize();//初始化python
    PyRun_SimpleString("print 'hello python'");//直接运行python代码
    Py_Finalize(); //释放python
    return;
}
void test1()
{
    Py_Initialize();//初始化python
    getcurrent();

    PyObject *pModule = NULL, *pFunc = NULL, *pArg = NULL;
    pModule = PyImport_ImportModule("demo");//引入模块
    pFunc = PyObject_GetAttrString(pModule, "print_arg");//直接获取模块中的函数
    pArg = Py_BuildValue("(s)", "hello_python"); //参数类型转换，传递一个字符串。将c/c++类型的字符串转换为python类型，元组中的python类型查看python文档
    PyEval_CallObject(pFunc, pArg); //调用直接获得的函数，并传递参数

    Py_Finalize(); //释放python
    return;
}
void test2()
{
    Py_Initialize();
    getcurrent();

    PyObject *pModule = NULL, *pDict = NULL, *pFunc = NULL, *pArg = NULL, *result = NULL;
    pModule = PyImport_ImportModule("demo"); //引入模块
    pDict = PyModule_GetDict(pModule); //获取模块字典属性 //相当于Python模块对象的__dict__ 属性，得到模块名称空间下的字典对象
    pFunc = PyDict_GetItemString(pDict, "add"); //从字典属性中获取函数
    pArg = Py_BuildValue("(i, i)", 1, 2); //参数类型转换，传递两个整型参数
    result = PyEval_CallObject(pFunc, pArg); //调用函数，并得到python类型的返回值
    int sum;
    PyArg_Parse(result, "i", &sum); //将python类型的返回值转换为c/c++类型
    printf("sum=%d\n", sum);

    Py_Finalize();
}
