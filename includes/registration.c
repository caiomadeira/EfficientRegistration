#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

#define ALPHA 26

#define FALSE 0
#define TRUE 1

struct client
{
	int id;
	char* name;
	char* cpf;
	char* email;
	struct client* next;
};
typedef struct client Client;

struct registration
{
	Client* clist[ALPHA];
};

typedef struct registration Registration;

Registration* createInstance(void);
Client* setClient(int id, char* name, char* cpf, char* email);
int push(Registration* r, int id, char* name, char* cpf, char* email);
void showRegFor(Registration* r, char letter);
void freeMemory(Registration* r);
char* allocStr(int n);
int len(char* s);
void copystr(char* s, char* t);

int len(char* s)
{
	if (*s == '\0')
		return 0;
	return 1 + len(s + 1);
}

void copystr(char* s, char* t)
{
	if (*t == '\0')
		*s = '\0';
	else
	{
		*s = *t;
		copystr(s + 1, t + 1);
	}
}

char* allocStr(int n)
{
	char* buffer = (char*)malloc((n + 1) * sizeof(char));
	if (buffer == NULL)
		return NULL;
	return buffer;
}

Registration* createInstance(void)
{
	Registration* r = (Registration*)malloc(sizeof(Registration));
	if (r != NULL)
	{
		for (int i = 0; i < ALPHA; i++)
		{
			r->clist[i] = NULL;
		}
	}
	printf("Instance registration created.\n");
	return r;
}

Client* setClient(int id, char* name, char* cpf, char* email)
{
	Client* newInstance = (Client*)malloc(sizeof(Client));
	if (newInstance == NULL)
		return NULL;

	newInstance->name = allocStr((int)len(name));
	newInstance->cpf = allocStr((int)len(cpf));
	newInstance->email = allocStr((int)len(email));
	if (newInstance->name == NULL || newInstance->cpf == NULL || newInstance->email == NULL)
	{
		free(newInstance->name);
		free(newInstance->cpf);
		free(newInstance->email);
		return NULL;
	}

	copystr(newInstance->name, name);
	copystr(newInstance->cpf, cpf);
	copystr(newInstance->email, email);

	newInstance->id = id;

	return newInstance;
}

int push(Registration* r, int id, char* name, char* cpf, char* email)
{
	int index = toupper(name[0]) - 'A'; // Preciso certificar de a primeira sempre vai estar em maiusculo
	Client* c = setClient(id, name, cpf, email);
	if (c == NULL)
		return 0;
	c->next = r->clist[index];
	r->clist[index] = c;
	return 1;
}

void showRegFor(Registration* r, char letter)
{
	Client* p;

	int find = 0;
	int index = letter - 'A';
	printf("%c:\n", letter);
	for (int i = 0; i < ALPHA; i++)
	{
		p = r->clist[i];
		if (i == index)
		{
			for (p; p != NULL; p = p->next)
			{
				find = 1;
				printf("  %s: %d %s %s\n", p->name, p->id, p->cpf, p->email);
			}
		}
	}

	if (p == NULL && find == 0)
		printf("  Sem clientes para esta letra.\n");
}

void showRegs(Registration* r)
{
	Client* p;
	for (int i = 0; i < ALPHA; i++)
	{
		printf("%c:\n", (i + 'A'));
		for (p = r->clist[i]; p != NULL; p = p->next)
		{
			printf("  %s: %d %s %s\n", p->name, p->id, p->cpf, p->email);
		}

		if (p == NULL)
		{
			printf("  NULL\n");
		}
	}
}

void freeMemory(Registration* r)
{
	Client* t, * p;
	for (int i = 0; i < ALPHA; i++)
	{
		p = r->clist[i];
		while (p != NULL)
		{
			t = p->next;
			free(p->name);
			free(p);
			p = t;
		}
	}
	free(r);
}