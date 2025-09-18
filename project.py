import json
import os

class Student:
    _id_counter = 1
    def __init__(self, name):
        self.id = Student._id_counter
        Student._id_counter += 1
        self.name = name
        self.subjects = {}
    def add_subject(self, subject, score):
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self.subjects[subject] = score
    def calculate_average(self):
        return sum(self.subjects.values()) / len(self.subjects) if self.subjects else 0
    def get_grade(self):
        avg = self.calculate_average()
        if avg >= 90: return "A"
        elif avg >= 75: return "B"
        elif avg >= 50: return "C"
        else: return "Fail"
    def to_dict(self): return {"id": self.id,"name": self.name,"subjects": self.subjects}
    @classmethod
    def from_dict(cls, data):
        s = cls(data["name"]); s.id = data["id"]; s.subjects = data["subjects"]; return s

class GradeManager:
    def __init__(self): self.students = []
    def add_student(self, name, subjects):
        s = Student(name)
        for subj, score in subjects.items(): 
            s.add_subject(subj, score)
        self.students.append(s); print(f" Added {name} (ID {s.id})")
    def update_scores(self, sid, subj, score):
        s = self.find_student(sid)
        if s: s.add_subject(subj, score); print(f" Updated {s.name} {subj} -> {score}")
        else: print("⚠️ Not found")
    def view_report(self, sid):
        s = self.find_student(sid)
        if s:
            print(f"\n Report for {s.name} (ID {s.id})")
            for sub, sc in s.subjects.items(): print(f"  {sub}: {sc}")
            print(f"  Avg: {s.calculate_average():.2f}  Grade: {s.get_grade()}\n")
        else: print(" Not found")
    def delete_student(self, sid):
        s = self.find_student(sid)
        if s: self.students.remove(s); print(f"🗑️ Deleted {s.name}")
        else: print(" Not found")
    def save_to_file(self, fn="grades.json"):
        with open(fn,"w") as f: json.dump([s.to_dict() for s in self.students],f,indent=2)
        print(" Saved")
    def load_from_file(self, fn="grades.json"):
        if os.path.exists(fn):
            with open(fn) as f: data=json.load(f)
            self.students=[Student.from_dict(d) for d in data]
            if self.students: Student._id_counter=max(s.id for s in self.students)+1
            print(" Loaded")
    def find_student(self,sid): return next((s for s in self.students if s.id==sid),None)

def main():
    gm=GradeManager(); gm.load_from_file()
    while True:
        print("\n1.Add  2.Update  3.Report  4.Delete  5.Save&Exit")
        ch=input("Choice: ")
        if ch=="1":
            name=input("Name: "); subs={}
            while True:
                subj=input("Subject (or done): ")
                if subj=="done": break
                score=int(input(f"{subj} score: ")); subs[subj]=score
            gm.add_student(name,subs)
        elif ch=="2":
            sid=int(input("ID: ")); subj=input("Subject: "); score=int(input("Score: "))
            gm.update_scores(sid,subj,score)
        elif ch=="3":
            sid=int(input("ID: ")); gm.view_report(sid)
        elif ch=="4":
            sid=int(input("ID: ")); gm.delete_student(sid)
        elif ch=="5":
            gm.save_to_file(); print("👋 Bye"); break
        else: print("⚠️ Invalid")

main()
