#include <iostream>
#include <windows.h>
#include <fstream> //导入地图文件有关的头文件。
#include <sstream> //同上
#include <tchar.h> // 解决 "const char *" 类型的实参与 "LPCWSTR" 类型的形参不兼容
using namespace std;

int map[40][50] = {0}; //储存地图
int mapX = 50;		   //地图x大小
int mapY = 40;		   //地图y大小
int start[2] = {10, 10};
int end_[2] = {15, 25};
int speed = 1; //限制打印的速度，防止一下子搞完了，为了视觉美观才加上的。建议范围0~50，数字越大程序运行越慢。单位是毫秒。

void ProgramBegin();   //初始化程序
void gotoxy(int, int); //跳转光标
void InMap();		   //将地图导入数组
void PrintMap();	   //打印地图
void FindMap();		   //////寻路

//*****初始化程序*****
void ProgramBegin()
{
	//改变窗口位置xy宽高xy
	char title[100];
	HWND hwnd;
	GetConsoleTitle(_T(title), 100);
	hwnd = FindWindow(NULL, _T(title));
	MoveWindow(hwnd, -5, 0, 1300, 700, TRUE);
	//隐藏光标
	CONSOLE_CURSOR_INFO cursor_info = {1, 0};
	SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
	system("cls"); //清屏
}

//*****跳转光标函数*****
void gotoxy(int x, int y)
{
	HANDLE hout;
	COORD coord;
	coord.X = x;
	coord.Y = y;
	hout = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hout, coord);
}

//*****将地图导入数组*****
void ImportMap()
{
	string str; //新建字符串
	int iy = 0;
	ifstream fin;
	fin.open("map1.txt"); //打开当前文件夹下的“map1.txt”文件
	while (!fin.eof())
	{
		getline(fin, str); //txt文本赋值给str
		for (int ix = 0; ix < mapX; ix++)
		{
			stringstream sss;
			sss << str[ix];
			sss >> map[iy][ix];
		}
		cout << endl;
		iy++;
	}
	fin.close(); //关闭txt文件
}

//*****打印地图*****
void PrintMap()
{
	int x = mapX;
	int y = mapY;
	for (int y = 0; y < mapY; y++)
	{
		for (int x = 0; x < mapX; x++)
		{

			if (map[y][x] == 1)
			{
				gotoxy(x * 2, y);
				cout << "█";
			}
			if (map[y][x] == 0)
			{
				gotoxy(x * 2, y);
				cout << "  ";
			}
		}
		cout << endl;
	}
}

//*****记录开始、结束点*****
void StartEnd()
{
	for (int y = 0; y < mapY; y++)
	{
		for (int x = 0; x < mapX; x++)
		{
			if (map[y][x] == 8) //找到出发点8，并记录在start[]里
			{
				start[0] = x;
				start[1] = y;
			}
			if (map[y][x] == 9) //找到终点9，并记录在end[]里
			{
				end_[0] = x;
				end_[1] = y;
			}
		}
	}
}

int main()
{
	ProgramBegin(); //初始化程序，定义控制台宽高等。
	ImportMap();	//从外界导入地图
	PrintMap();		//打印地图
	StartEnd();		//查询地图中的开始结束点

	FindMap(); /////////正菜：寻路算法。

	Sleep(1000000); //卡死程序，防止打印完立马退出。
	return 0;
}

////重头戏：寻路代码本体！！
void FindMap()
{
	int road[40][50][4] = {0}; //road:[该格y坐标][x][0原来地图，1父x，2父y，3迭代等级]
	gotoxy(start[0] * 2, start[1]);
	cout << "start";
	gotoxy(end_[0] * 2, end_[1]);
	cout << "end_";
	road[start[1]][start[0]][3] = 1;
	road[end_[1]][end_[0]][3] = 99999;
	for (int y = 0; y < mapY; y++) //将地图复制进road数组，其实不这么做也行的。
	{
		for (int x = 0; x < mapX; x++)
		{
			road[y][x][0] = map[y][x];
			gotoxy(x * 2, y);
		}
	}
	int i = 1;
	int x, y;
	while (1) //正式寻路的第一步，“洪水式”遍历每一个点。
	{
		for (y = 1; y < mapY - 1; y++) //遍历每一个点
		{
			for (x = 1; x < mapX - 1; x++)
			{
				if (road[y][x][3] == i) //遍历地图，找到一个“当前迭代等级的有效点”
				{
					for (int fy = -1; fy <= 1; fy++) //在该点上下左右探索
					{
						for (int fx = -1; fx <= 1; fx++)
						{
							if ((fx == 0 && fy != 0) || (fx != 0 && fy == 0)) //只要上下左右，排除对角及中心
							{
								if (road[y + fy][x + fx][3] == 99999) //若找到“终点”99999
								{
									road[y + fy][x + fx][1] = x; //记录下“父点”的坐标
									road[y + fy][x + fx][2] = y;
									x = x + fx;
									y = y + fy;
									i++;
									road[y][x][3] == i; //“终点”赋值为最终迭代数 i
									goto success1;		//跳转到外面
								}
								else if (road[y + fy][x + fx][0] == 0 && road[y + fy][x + fx][3] == 0) //若找到个“安全的派生点”
								{
									road[y + fy][x + fx][3] = i + 1; //则将该点加入有效点，且它迭代等级+1
									road[y + fy][x + fx][1] = x;
									road[y + fy][x + fx][2] = y;
									gotoxy((x + fx) * 2, y + fy);
									cout << (i + 1) % 10; //只打印个位数，防止数字过多杂乱。
								}
							}
						}
					}
				}
			}
		}
		Sleep(speed);
		i++;
	}
success1:	  //上面的跳转到这
	while (1) //正式寻路的第二步，跟着“父点”从终点开始一级一级逆向找到出发点。
	{
	comehome:
		for (int fy = -1; fy <= 1; fy++) //在点上下左右探索
		{
			for (int fx = -1; fx <= 1; fx++)
			{
				if ((fx == 0 && fy != 0) || (fx != 0 && fy == 0)) //只要上下左右，排除对角及中心
				{
					if (road[y + fy][x + fx][3] == 1)							 //若找到“原点”，回家；
						goto success2;											 //跳转到外面
					else if (road[y][x][1] == x + fx && road[y][x][2] == y + fy) //若找到“父点”
					{
						x = x + fx;
						y = y + fy;
						gotoxy(x * 2, y);
						cout << "▓"; //打印路径：“@”
						Sleep(speed);
						goto comehome;
					}
				}
			}
		}
	}
success2:							//上面的跳转到这
	gotoxy(start[0] * 2, start[1]); //补打印一下开始结束点
	cout << "start";
	gotoxy(end_[0] * 2, end_[1]);
	cout << "end_";
}
