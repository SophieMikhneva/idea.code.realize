export interface Discipline {
  id: number;
  title: string;
  lecturer: string;
  rating: number;
  documents: {
    presentations: Presentation[];
    abstract: string;
    cheatSheet: string;
  };
}

export interface Presentation {
  id: number;
  title: string;
  description: string;
  authorId: number;
  subjectId: number;
  groupId: number;
  uploadDate: Date;
  lastModified: Date;
  fileName: string;
  fileType: string;
}

export type Document = Presentation | "Abstract" | "CheatSheet";
