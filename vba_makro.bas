Attribute VB_Name = "KostenstellenVerteilung"

' ============================================================================
' HAUPT-PROZEDUR: Verteilung berechnen
' ============================================================================
Sub BerechneVerteilung()
    Dim wsKostenstellen As Worksheet
    Dim wsRechnung As Worksheet
    Dim wsErgebnis As Worksheet
    Dim letzteZeileKS As Long
    Dim letzteZeileRechnung As Long
    Dim i As Long, j As Long
    Dim kostenstellenDict As Object
    Dim ergebnisDict As Object
    Dim posBezeichnung As String
    Dim betrag As Double
    Dim verteilungsart As String
    Dim zielKSText As String
    Dim zielKSArray() As String
    Dim anzahlKS As Integer
    Dim anteil As Double
    Dim nettoBetrag As Double
    Dim bruttoBetrag As Double
    Dim eingabeModus As String
    Dim anzeigeModus As String
    Dim summeNetto As Double
    Dim summeBrutto As Double
    
    ' Initialisiere Dictionaries
    Set kostenstellenDict = CreateObject("Scripting.Dictionary")
    Set ergebnisDict = CreateObject("Scripting.Dictionary")
    
    ' Setze Referenzen auf die Worksheets
    Set wsKostenstellen = ThisWorkbook.Sheets("Kostenstellen")
    Set wsRechnung = ThisWorkbook.Sheets("Rechnung")
    Set wsErgebnis = ThisWorkbook.Sheets("Ergebnis")
    
    ' Hole Einstellungen (kann später aus UserForm kommen)
    eingabeModus = "netto"  ' "netto" oder "brutto"
    anzeigeModus = "netto"  ' "netto" oder "brutto"
    
    ' ============================================================================
    ' 1. KOSTENSTELLENLISTE LADEN
    ' ============================================================================
    letzteZeileKS = wsKostenstellen.Cells(wsKostenstellen.Rows.Count, "A").End(xlUp).Row
    
    For i = 2 To letzteZeileKS
        Dim ksNummer As Variant
        Dim ksBezeichnung As String
        
        ksNummer = wsKostenstellen.Cells(i, "A").Value
        ksBezeichnung = wsKostenstellen.Cells(i, "B").Value
        
        If Not IsEmpty(ksNummer) And IsNumeric(ksNummer) Then
            kostenstellenDict(ksNummer) = ksBezeichnung
            ' Initialisiere Ergebnis-Dictionary
            ergebnisDict(ksNummer) = Array(0#, 0#, "")  ' Netto, Brutto, Positionen
        End If
    Next i
    
    ' ============================================================================
    ' 2. RECHNUNGSPOSITIONEN VERARBEITEN
    ' ============================================================================
    letzteZeileRechnung = wsRechnung.Cells(wsRechnung.Rows.Count, "A").End(xlUp).Row
    
    For i = 2 To letzteZeileRechnung
        posBezeichnung = wsRechnung.Cells(i, "A").Value
        betrag = 0
        verteilungsart = wsRechnung.Cells(i, "C").Value
        zielKSText = wsRechnung.Cells(i, "D").Value
        
        ' Betrag einlesen
        If IsNumeric(wsRechnung.Cells(i, "B").Value) Then
            betrag = CDbl(wsRechnung.Cells(i, "B").Value)
        Else
            GoTo NaechstePosition
        End If
        
        ' Wenn Eingabe Brutto war, zuerst in Netto umrechnen
        If eingabeModus = "brutto" Then
            nettoBetrag = betrag / 1.19
        Else
            nettoBetrag = betrag
        End If
        
        ' Ziel-Kostenstellen parsen
        If verteilungsart = "Einzelne Kostenstelle" Then
            ' Kommagetrennte Liste aus Spalte D
            zielKSArray = Split(zielKSText, ",")
            anzahlKS = 0
            
            For j = LBound(zielKSArray) To UBound(zielKSArray)
                Dim ks As Variant
                ks = Trim(zielKSArray(j))
                If IsNumeric(ks) Then
                    ks = CDbl(ks)
                    If kostenstellenDict.Exists(ks) Then
                        anzahlKS = anzahlKS + 1
                        anteil = nettoBetrag / anzahlKS
                        
                        ' Auf alle Ziel-KS verteilen
                        Dim k As Variant
                        For k = LBound(zielKSArray) To UBound(zielKSArray)
                            Dim ks2 As Variant
                            ks2 = Trim(zielKSArray(k))
                            If IsNumeric(ks2) Then
                                ks2 = CDbl(ks2)
                                If kostenstellenDict.Exists(ks2) Then
                                    ergebnisDict(ks2)(0) = ergebnisDict(ks2)(0) + anteil
                                    ergebnisDict(ks2)(1) = ergebnisDict(ks2)(1) + (anteil * 1.19)
                                    ergebnisDict(ks2)(2) = ergebnisDict(ks2)(2) & posBezeichnung & "; "
                                End If
                            End If
                        Next k
                        Exit For
                    End If
                End If
            Next j
            
        ElseIf verteilungsart = "Gleichmäßig auf alle Kostenstellen" Then
            ' Auf ALLE Kostenstellen verteilen
            anzahlKS = kostenstellenDict.Count
            anteil = nettoBetrag / anzahlKS
            
            For Each k In kostenstellenDict.Keys
                ergebnisDict(k)(0) = ergebnisDict(k)(0) + anteil
                ergebnisDict(k)(1) = ergebnisDict(k)(1) + (anteil * 1.19)
                ergebnisDict(k)(2) = ergebnisDict(k)(2) & posBezeichnung & "; "
            Next k
            
        ElseIf verteilungsart = "Gleichmäßig auf verwendete Kostenstellen" Then
            ' Nur auf die in Spalte D eingetragenen Kostenstellen
            zielKSArray = Split(zielKSText, ",")
            anzahlKS = 0
            
            For j = LBound(zielKSArray) To UBound(zielKSArray)
                Dim ks3 As Variant
                ks3 = Trim(zielKSArray(j))
                If IsNumeric(ks3) Then
                    ks3 = CDbl(ks3)
                    If kostenstellenDict.Exists(ks3) Then
                        anzahlKS = anzahlKS + 1
                    End If
                End If
            Next j
            
            If anzahlKS > 0 Then
                anteil = nettoBetrag / anzahlKS
                
                For j = LBound(zielKSArray) To UBound(zielKSArray)
                    Dim ks4 As Variant
                    ks4 = Trim(zielKSArray(j))
                    If IsNumeric(ks4) Then
                        ks4 = CDbl(ks4)
                        If kostenstellenDict.Exists(ks4) Then
                            ergebnisDict(ks4)(0) = ergebnisDict(ks4)(0) + anteil
                            ergebnisDict(ks4)(1) = ergebnisDict(ks4)(1) + (anteil * 1.19)
                            ergebnisDict(ks4)(2) = ergebnisDict(ks4)(2) & posBezeichnung & "; "
                        End If
                    End If
                Next j
            End If
        End If
        
NaechstePosition:
    Next i
    
    ' ============================================================================
    ' 3. ERGEBNIS SCHREIBEN
    ' ============================================================================
    ' Lösche alte Ergebnisse
    wsErgebnis.Cells.Clear
    
    ' Schreibe Kopfzeile
    wsErgebnis.Cells(1, 1) = "Kostenstelle"
    wsErgebnis.Cells(1, 2) = "Bezeichnung"
    wsErgebnis.Cells(1, 3) = "Netto (€)"
    wsErgebnis.Cells(1, 4) = "Brutto (€)"
    wsErgebnis.Cells(1, 5) = "Zugewiesene Positionen"
    
    ' Formatiere Kopfzeile
    With wsErgebnis.Range("A1:E1")
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(255, 140, 0)
    End With
    
    ' Schreibe Daten
    Dim zeile As Long
    zeile = 2
    summeNetto = 0
    summeBrutto = 0
    
    For Each k In ergebnisDict.Keys
        If ergebnisDict(k)(0) > 0.01 Or ergebnisDict(k)(1) > 0.01 Then
            wsErgebnis.Cells(zeile, 1) = k
            wsErgebnis.Cells(zeile, 2) = kostenstellenDict(k)
            wsErgebnis.Cells(zeile, 3) = Round(ergebnisDict(k)(0), 2)
            wsErgebnis.Cells(zeile, 4) = Round(ergebnisDict(k)(1), 2)
            wsErgebnis.Cells(zeile, 5) = Left(ergebnisDict(k)(2), Len(ergebnisDict(k)(2)) - 2)  ' Letztes "; " entfernen
            
            summeNetto = summeNetto + ergebnisDict(k)(0)
            summeBrutto = summeBrutto + ergebnisDict(k)(1)
            zeile = zeile + 1
        End If
    Next k
    
    ' ============================================================================
    ' 4. GESAMTSUMME
    ' ============================================================================
    zeile = zeile + 1
    wsErgebnis.Cells(zeile, 1) = "GESAMT"
    wsErgebnis.Cells(zeile, 1).Font.Bold = True
    
    If anzeigeModus = "brutto" Then
        wsErgebnis.Cells(zeile, 4) = Round(summeBrutto, 2)
        wsErgebnis.Cells(zeile, 4).Font.Bold = True
    Else
        wsErgebnis.Cells(zeile, 3) = Round(summeNetto, 2)
        wsErgebnis.Cells(zeile, 3).Font.Bold = True
    End If
    
    ' Spaltenbreite anpassen
    wsErgebnis.Columns("A").ColumnWidth = 15
    wsErgebnis.Columns("B").ColumnWidth = 30
    wsErgebnis.Columns("C").ColumnWidth = 15
    wsErgebnis.Columns("D").ColumnWidth = 15
    wsErgebnis.Columns("E").ColumnWidth = 40
    
    MsgBox "✅ Verteilung berechnet!" & vbCrLf & vbCrLf & _
           "Gesamtsumme (Netto): " & Format(summeNetto, "#,##0.00") & " €" & vbCrLf & _
           "Gesamtsumme (Brutto): " & Format(summeBrutto, "#,##0.00") & " €", _
           vbInformation, "Berechnung abgeschlossen"
End Sub

' ============================================================================
' HILFSPROZEDUR: Alle Positionen löschen
' ============================================================================
Sub LoeschePositionen()
    Dim wsRechnung As Worksheet
    Set wsRechnung = ThisWorkbook.Sheets("Rechnung")
    
    ' Lösche alle Zeilen ab Zeile 2
    wsRechnung.Range("A2:E100").ClearContents
    
    MsgBox "✅ Alle Positionen gelöscht!", vbInformation
End Sub

' ============================================================================
' HILFSPROZEDUR: Ergebnis löschen
' ============================================================================
Sub LoescheErgebnis()
    Dim wsErgebnis As Worksheet
    Set wsErgebnis = ThisWorkbook.Sheets("Ergebnis")
    
    wsErgebnis.Cells.Clear
    
    MsgBox "✅ Ergebnis gelöscht!", vbInformation
End Sub