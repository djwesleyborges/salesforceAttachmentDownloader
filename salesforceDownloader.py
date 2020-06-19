import json
import pyodbc
import requests
from datetime import timedelta, datetime
from simple_salesforce import Salesforce
from dateutil.relativedelta import relativedelta


def connectionSalesForce():
    # Login SalesForce
    loginInfo = json.load(open('login.json'))
    username = loginInfo["username"]
    password = loginInfo["password"]
    security_token = loginInfo["security_token"]
    # Make SalesForce connection
    sf = Salesforce(username, password, security_token)
    return sf


def fetchAttachment(attachmentId):
    """
    Get attachment
    :param attachmentId
    """
    conn = connectionSalesForce()
    instanceSF = conn.sf_instance
    tokenBearer = conn.headers

    response = requests.get(
        'https://' + instanceSF + '/services/data/v42.0/sobjects/Attachment/' + attachmentId + '/body',
        headers=tokenBearer)
    # binary file
    attachmentBodyByte = response.content
    # attachmentBody = str(base64.b64encode(attachmentBodyByte))
    return attachmentBodyByte


def queryAttachent(firstDay):
    """
    :param: first Day of Month
    Return the attachments of day between 00:00:00H and 23:59:59H
    """
    start = (firstDay + "T" + "00:00:00Z")
    end = (firstDay + "T" + "23:59:59Z")

    sf = connectionSalesForce()
    # SQL
    query = "Select Body, BodyLength, ContentType, CreatedById, CreatedDate," \
            " Description, Id, IsDeleted, IsPrivate, LastModifiedById, LastModifiedDate," \
            " Name, OwnerId, ParentId, Parent.Type, SystemModstamp " \
            f"FROM Attachment where CreatedDate > {start} and CreatedDate < {end}"

    attachmentQuery = sf.query(query)

    attachmentList = list()
    if attachmentQuery.get('totalSize') == 0:
        return None
    else:
        for attachment in attachmentQuery.get('records'):
            attachmentList.append(attachment)
        return attachmentList


def connDataBase():
    """
    connection with database
    :return: connectionDB
    """
    server = "HOSTNAME\SQLEXPRESS"
    database = "DATABASE"

    connectionString = "Driver={SQL Server Native Client 11.0};Server=" + server + ";Database=" + database + ";Trusted_Connection=yes;"
    connection = pyodbc.connect(connectionString)
    return connection.cursor()


def getAttachments(attachmentList):
    """
    :param list of attachments
    Insert attachment in DataBase
    """

    cursor = connDataBase()

    for att in attachmentList:
        attachmentId = att.get('Id')
        attachmentName = att.get('Name')
        attachmentBodyLength = att.get('BodyLength')
        attachmentContentType = att.get('ContentType')
        attachmentCreatedById = att.get('CreatedById')
        attachmentCreatedDate = att.get('CreatedDate')
        attachmentDescription = att.get('Description')
        attachmentIsDeleted = att.get('IsDeleted')
        attachmentIsPrivate = att.get('IsPrivate')
        attachmentLastModifiedById = att.get('LastModifiedById')
        attachmentLastModifiedDate = att.get('LastModifiedDate')
        attachmentOwnerId = att.get('OwnerId')
        attachmentParentId = att.get('ParentId')
        if att.get('Parent') is None:
            attachmentParentType = 'None'
        else:
            attachmentParentType = att.get('Parent').get('Type')
        attachmentSystemModstamp = att.get('SystemModstamp')
        print(f"Baixando anexo {attachmentName}")

        # Get attachment
        attachmentBodyByte = fetchAttachment(attachmentId)

        paramsInsert = (attachmentId, attachmentIsDeleted, attachmentParentId,
                        attachmentName, attachmentIsPrivate, attachmentContentType,
                        attachmentBodyLength, attachmentBodyByte, attachmentOwnerId,
                        attachmentCreatedDate, attachmentCreatedById, attachmentLastModifiedDate,
                        attachmentLastModifiedById, attachmentSystemModstamp, attachmentDescription,
                        attachmentParentType)
        try:
            cursor.execute(
                "INSERT INTO dbo.Attachment ([Id],[IsDeleted],[ParentId],[Name],[IsPrivate],[ContentType],"
                "[BodyLength],[Body],[OwnerId],[CreatedDate],[CreatedById],[LastModifiedDate],[LastModifiedById],"
                "[SystemModstamp],[Description],[ParentType]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                paramsInsert)
            cursor.commit()
            print(f"Inserted file {attachmentName} in the database")
        except Exception as e:
            print(e)
    connDataBase().close()


def main():
    startProgram = datetime.now()
    firstDay = "01-02-2020"

    start = datetime.strptime(firstDay, "%d-%m-%Y")
    end = (start + relativedelta(months=+1)) - timedelta(days=1)
    date_generated = [start + timedelta(days=x) for x in range(0, end.day)]

    for d in date_generated:
        # converte date to str
        date = d.strftime("%Y-%m-%d")
        result = queryAttachent(date)
        if result != None:
            getAttachments(result)

    print(f"Inserted attachment of month: {firstDay[3:5]} year {firstDay[6:10]}")

    endProgram = datetime.now()

    print(f"Program started in {startProgram} and finished in {endProgram}")


main()
