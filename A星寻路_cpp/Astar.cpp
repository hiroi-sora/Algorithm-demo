#include <iostream>
#include <windows.h>
#include <fstream> //�����ͼ�ļ��йص�ͷ�ļ���
#include <sstream> //ͬ��
#include <tchar.h> // ��� "const char *" ���͵�ʵ���� "LPCWSTR" ���͵��ββ�����
using namespace std;

int map[40][50] = {0}; //�����ͼ
int mapX = 50;		   //��ͼx��С
int mapY = 40;		   //��ͼy��С
int start[2] = {10, 10};
int end_[2] = {15, 25};
int speed = 1; //���ƴ�ӡ���ٶȣ���ֹһ���Ӹ����ˣ�Ϊ���Ӿ����۲ż��ϵġ����鷶Χ0~50������Խ���������Խ������λ�Ǻ��롣

void ProgramBegin();   //��ʼ������
void gotoxy(int, int); //��ת���
void InMap();		   //����ͼ��������
void PrintMap();	   //��ӡ��ͼ
void FindMap();		   //////Ѱ·

//*****��ʼ������*****
void ProgramBegin()
{
	//�ı䴰��λ��xy���xy
	char title[100];
	HWND hwnd;
	GetConsoleTitle(_T(title), 100);
	hwnd = FindWindow(NULL, _T(title));
	MoveWindow(hwnd, -5, 0, 1300, 700, TRUE);
	//���ع��
	CONSOLE_CURSOR_INFO cursor_info = {1, 0};
	SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
	system("cls"); //����
}

//*****��ת��꺯��*****
void gotoxy(int x, int y)
{
	HANDLE hout;
	COORD coord;
	coord.X = x;
	coord.Y = y;
	hout = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hout, coord);
}

//*****����ͼ��������*****
void ImportMap()
{
	string str; //�½��ַ���
	int iy = 0;
	ifstream fin;
	fin.open("map1.txt"); //�򿪵�ǰ�ļ����µġ�map1.txt���ļ�
	while (!fin.eof())
	{
		getline(fin, str); //txt�ı���ֵ��str
		for (int ix = 0; ix < mapX; ix++)
		{
			stringstream sss;
			sss << str[ix];
			sss >> map[iy][ix];
		}
		cout << endl;
		iy++;
	}
	fin.close(); //�ر�txt�ļ�
}

//*****��ӡ��ͼ*****
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
				cout << "��";
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

//*****��¼��ʼ��������*****
void StartEnd()
{
	for (int y = 0; y < mapY; y++)
	{
		for (int x = 0; x < mapX; x++)
		{
			if (map[y][x] == 8) //�ҵ�������8������¼��start[]��
			{
				start[0] = x;
				start[1] = y;
			}
			if (map[y][x] == 9) //�ҵ��յ�9������¼��end[]��
			{
				end_[0] = x;
				end_[1] = y;
			}
		}
	}
}

int main()
{
	ProgramBegin(); //��ʼ�����򣬶������̨��ߵȡ�
	ImportMap();	//����絼���ͼ
	PrintMap();		//��ӡ��ͼ
	StartEnd();		//��ѯ��ͼ�еĿ�ʼ������

	FindMap(); /////////���ˣ�Ѱ·�㷨��

	Sleep(1000000); //�������򣬷�ֹ��ӡ�������˳���
	return 0;
}

////��ͷϷ��Ѱ·���뱾�壡��
void FindMap()
{
	int road[40][50][4] = {0}; //road:[�ø�y����][x][0ԭ����ͼ��1��x��2��y��3�����ȼ�]
	gotoxy(start[0] * 2, start[1]);
	cout << "start";
	gotoxy(end_[0] * 2, end_[1]);
	cout << "end_";
	road[start[1]][start[0]][3] = 1;
	road[end_[1]][end_[0]][3] = 99999;
	for (int y = 0; y < mapY; y++) //����ͼ���ƽ�road���飬��ʵ����ô��Ҳ�еġ�
	{
		for (int x = 0; x < mapX; x++)
		{
			road[y][x][0] = map[y][x];
			gotoxy(x * 2, y);
		}
	}
	int i = 1;
	int x, y;
	while (1) //��ʽѰ·�ĵ�һ��������ˮʽ������ÿһ���㡣
	{
		for (y = 1; y < mapY - 1; y++) //����ÿһ����
		{
			for (x = 1; x < mapX - 1; x++)
			{
				if (road[y][x][3] == i) //������ͼ���ҵ�һ������ǰ�����ȼ�����Ч�㡱
				{
					for (int fy = -1; fy <= 1; fy++) //�ڸõ���������̽��
					{
						for (int fx = -1; fx <= 1; fx++)
						{
							if ((fx == 0 && fy != 0) || (fx != 0 && fy == 0)) //ֻҪ�������ң��ų��ԽǼ�����
							{
								if (road[y + fy][x + fx][3] == 99999) //���ҵ����յ㡱99999
								{
									road[y + fy][x + fx][1] = x; //��¼�¡����㡱������
									road[y + fy][x + fx][2] = y;
									x = x + fx;
									y = y + fy;
									i++;
									road[y][x][3] == i; //���յ㡱��ֵΪ���յ����� i
									goto success1;		//��ת������
								}
								else if (road[y + fy][x + fx][0] == 0 && road[y + fy][x + fx][3] == 0) //���ҵ�������ȫ�������㡱
								{
									road[y + fy][x + fx][3] = i + 1; //�򽫸õ������Ч�㣬���������ȼ�+1
									road[y + fy][x + fx][1] = x;
									road[y + fy][x + fx][2] = y;
									gotoxy((x + fx) * 2, y + fy);
									cout << (i + 1) % 10; //ֻ��ӡ��λ������ֹ���ֹ������ҡ�
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
success1:	  //�������ת����
	while (1) //��ʽѰ·�ĵڶ��������š����㡱���յ㿪ʼһ��һ�������ҵ������㡣
	{
	comehome:
		for (int fy = -1; fy <= 1; fy++) //�ڵ���������̽��
		{
			for (int fx = -1; fx <= 1; fx++)
			{
				if ((fx == 0 && fy != 0) || (fx != 0 && fy == 0)) //ֻҪ�������ң��ų��ԽǼ�����
				{
					if (road[y + fy][x + fx][3] == 1)							 //���ҵ���ԭ�㡱���ؼң�
						goto success2;											 //��ת������
					else if (road[y][x][1] == x + fx && road[y][x][2] == y + fy) //���ҵ������㡱
					{
						x = x + fx;
						y = y + fy;
						gotoxy(x * 2, y);
						cout << "��"; //��ӡ·������@��
						Sleep(speed);
						goto comehome;
					}
				}
			}
		}
	}
success2:							//�������ת����
	gotoxy(start[0] * 2, start[1]); //����ӡһ�¿�ʼ������
	cout << "start";
	gotoxy(end_[0] * 2, end_[1]);
	cout << "end_";
}
